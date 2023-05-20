import pygame
from pygame.locals import*
import card_test
import random

# modified the size to be 800x800, 1000x1000 went off screen for me
size = width, height = (900, 900)

#initializaion stuff
pygame.init()
running = True
clock = pygame.time.Clock()
message_end_time = pygame.time.get_ticks() + 3000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Monopoly")
font = pygame.font.SysFont(None, 20)


#board
boardImg = pygame.image.load('assets/board.png').convert()
boardImg = pygame.transform.scale(boardImg, (int(width*0.7), int(height*0.7)))
board_rect = boardImg.get_rect(center=screen.get_rect().center)


# card test buttons
chancetest = pygame.image.load('assets/chance_test.png').convert()
commtest = pygame.image.load('assets/comm_test.png').convert()
# rect (left, top, width, height)
commtest_rect = commtest.get_rect() # Gets dimension of card image for button
chancetest_rect = chancetest.get_rect()

# Create rotated surfaces for the button images
commtest_rotated = pygame.transform.rotate(commtest, 400)
chancetest_rotated = pygame.transform.rotate(chancetest, 45)

# Get the dimensions of the rotated button images
commtest_rotated_rect = commtest_rotated.get_rect()
chancetest_rotated_rect = chancetest_rotated.get_rect()

# Update the position and size of the button rectangles based on the rotated image dimensions
#commbutton = pygame.Rect(width*(1/11+0.02), height*(1/11+0.02), commtest_rotated_rect.width, commtest_rotated_rect.height)
#chancebutton = pygame.Rect(width*(10/11-0.02)-chancetest_rotated_rect.width, height*(1/11+0.02), chancetest_rotated_rect.width, chancetest_rotated_rect.height)

commbutton = pygame.Rect(width*(10/11-0.02)-commtest_rotated_rect.width, height*(1/11+0.02), commtest_rotated_rect.width, commtest_rotated_rect.height)
chancebutton = pygame.Rect(width*(1/11+0.02), height*(10/11-0.02)-chancetest_rotated_rect.height, chancetest_rotated_rect.width, chancetest_rotated_rect.height)

# will show card drawn
text = font.render(" ", False, (0,0,0))

def to_pointer(value): # dereference with retval[0]
	return [value]

class Player:	# name
	position = 15
	money = 2500
	in_jail = False
	name = ""
	eliminated = False

class PropertyTile:	# name, color, cost, house price, penalties
	tile_id = 0
	tile_type = "PropertyTile"
	house_count = 0
	owner = None

	name = ""
	color = ""
	cost = 0
	house_price = 0
	penalties = []

	def __init__(self, given_name, given_color, given_cost, given_price, given_penalties):
		self.name = given_name
		self.color = given_color
		self.cost = given_cost
		self.house_price = given_price
		self.penalties = given_penalties

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		pygame.draw.rect(screen, self.banner_c, self.banner, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))
		screen.blit(self.cost_text, (self.outline.centerx-self.cost_text.get_rect().width/2, self.outline.y+height*(1/11)-self.cost_text.get_rect().height))
		i = 0
		for x in self.house_squares:
			if self.house_count < 5:
				if self.house_count == 0 or i > self.house_count:
					pygame.draw.rect(screen, (58, 63, 71), x, 0)
				else:
					pygame.draw.rect(screen, (23, 163, 60), x, 0)
			else:
				pygame.draw.rect(screen, (186, 31, 0), x, 0)
			i = i + 1

class RailroadTile:	# name, cost
	tile_id = 0
	tile_type = "RailroadTile"
	owner = None

	name = ""
	cost = 0

	def __init__(self, given_name, given_cost):
		self.name = given_name
		self.cost = given_cost

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))
		screen.blit(self.cost_text, (self.outline.centerx-self.cost_text.get_rect().width/2, self.outline.y+height*(1/11)-self.cost_text.get_rect().height))

class CardTile:	# name (just the card type)
	tile_id = 0
	tile_type = "CardTile"

	name = ""

	def __init__(self, given_name):
		self.name = given_name

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))

class TaxTile:	# name, penalty
	tile_id = 0
	tile_type = "TaxTile"

	name = ""
	penalty = 0

	def __init__(self, given_name, given_penalty):
		self.name = given_name
		self.penalty = given_penalty

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))

class CornerTile:	# name, sends to prison?
	tile_id = 0
	tile_type = "CornerTile"

	name = ""
	sends_to_prison = False

	def __init__(self, given_name, given_bool):
		self.name = given_name
		self.sends_to_prison = given_bool

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))

class UtilityTile:	# name, cost
	tile_id = 0
	tile_type = "UtilityTile"
	owner = None

	name = ""
	cost = 0

	def __init__(self, given_name, given_cost):
		self.name = given_name
		self.cost = given_cost

	def draw(self):
		pygame.draw.rect(screen, (57, 196, 150), self.outline, 0)
		screen.blit(self.name_text, (self.outline.centerx-self.name_text.get_rect().width/2, self.outline.y+self.name_text.get_rect().height/3.5))

class Board:
	mortgage_rate = 0.5	# property cost * mortgage_rate = money received for mortgaging
	monopoly_rate = 2	# rent with 0 houses * monopoly_rate = money received (only applies if you have a monopoly with no houses on the tile)
	railroad_rate = [25, 50, 100, 200]	# cost of rent, depends on how many railroads are owned
	tiles = []
	players = []

	def add_player(self, name):
		new_player = Player()
		new_player.name = name
		self.players.append(to_pointer(new_player))
    
	def eliminate_player(self, player):
		for prop in self.tiles:
			if prop[0].owner == player:
				prop[0].owner = None
				prop[0].house_count = 0
		player.eliminated = True

	def initialize(self):
		self.tiles.append(to_pointer(CornerTile("Go", False)))
		self.tiles.append(to_pointer(PropertyTile("Medit. Ave", "Brown", 60, 50, [2, 10, 30, 90, 160, 250])))
		self.tiles.append(to_pointer(CardTile("Comm Chest")))
		self.tiles.append(to_pointer(PropertyTile("Baltic Ave", "Brown", 60, 50, [4, 20, 60, 180, 320, 450])))
		self.tiles.append(to_pointer(TaxTile("Income Tax", 200)))
		self.tiles.append(to_pointer(RailroadTile("Reading Rail", 200)))
		self.tiles.append(to_pointer(PropertyTile("Oriental Ave", "Cyan", 100, 50, [6, 30, 90, 270, 400, 550])))
		self.tiles.append(to_pointer(CardTile("Chance")))
		self.tiles.append(to_pointer(PropertyTile("Vermont Ave", "Cyan", 100, 50, [6, 30, 90, 270, 400, 550])))
		self.tiles.append(to_pointer(PropertyTile("Conn. Ave", "Cyan", 120, 50, [8, 40, 100, 300, 450, 600])))
		self.tiles.append(to_pointer(CornerTile("Visiting Jail", False)))
		self.tiles.append(to_pointer(PropertyTile("St. Charles", "Pink", 140, 100, [10, 50, 150, 450, 625, 750])))
		self.tiles.append(to_pointer(UtilityTile("Electric Co.", 150)))
		self.tiles.append(to_pointer(PropertyTile("States Ave", "Pink", 140, 100, [10, 50, 150, 450, 625, 750])))
		self.tiles.append(to_pointer(PropertyTile("Virginia Ave", "Pink", 160, 100, [12, 60, 180, 500, 700, 900])))
		self.tiles.append(to_pointer(RailroadTile("Penn. Rail", 200)))
		self.tiles.append(to_pointer(PropertyTile("St. James", "Orange", 180, 100, [14, 70, 200, 550, 750, 950])))
		self.tiles.append(to_pointer(CardTile("Comm Chest")))
		self.tiles.append(to_pointer(PropertyTile("Tenn. Ave", "Orange", 180, 100, [14, 70, 200, 550, 750, 950])))
		self.tiles.append(to_pointer(PropertyTile("New York St.", "Orange", 200, 100, [16, 80, 220, 600, 800, 1000])))
		self.tiles.append(to_pointer(CornerTile("Free Parking", False)))
		self.tiles.append(to_pointer(PropertyTile("Kent. Ave", "Red", 220, 150, [18, 90, 250, 700, 875, 1050])))
		self.tiles.append(to_pointer(CardTile("Chance")))
		self.tiles.append(to_pointer(PropertyTile("Indiana Ave", "Red", 220, 150, [18, 90, 250, 700, 875, 1050])))
		self.tiles.append(to_pointer(PropertyTile("Illinois Ave", "Red", 240, 150, [20, 100, 300, 750, 925, 1100])))
		self.tiles.append(to_pointer(RailroadTile("B&O Rail", 200)))
		self.tiles.append(to_pointer(PropertyTile("Atlantic Ave", "Yellow", 260, 150, [22, 110, 330, 800, 975, 1150])))
		self.tiles.append(to_pointer(PropertyTile("Ventnor Ave", "Yellow", 260, 150, [22, 110, 330, 800, 975, 1150])))
		self.tiles.append(to_pointer(UtilityTile("Water Works", 150)))
		self.tiles.append(to_pointer(PropertyTile("Marvin Ave", "Yellow", 280, 150, [24, 120, 360, 850, 1025, 1200])))
		self.tiles.append(to_pointer(CornerTile("Go to Jail", True)))
		self.tiles.append(to_pointer(PropertyTile("Pacific Ave", "Green", 300, 200, [26, 130, 390, 900, 1100, 1275])))
		self.tiles.append(to_pointer(PropertyTile("NC Ave", "Green", 300, 200, [26, 130, 390, 900, 1100, 1275])))
		self.tiles.append(to_pointer(CardTile("Comm Chest")))
		self.tiles.append(to_pointer(PropertyTile("Pacific Ave", "Green", 320, 200, [28, 150, 450, 1000, 1200, 1400])))
		self.tiles.append(to_pointer(RailroadTile("Short Line", 200)))
		self.tiles.append(to_pointer(CardTile("Chance")))
		self.tiles.append(to_pointer(PropertyTile("Park Place", "Blue", 350, 200, [35, 175, 500, 1100, 1300, 1500])))
		self.tiles.append(to_pointer(TaxTile("Luxury Tax", 75)))
		self.tiles.append(to_pointer(PropertyTile("Boardwalk", "Blue", 400, 200, [50, 200, 600, 1400, 1700, 2000])))

	def draw_chest(self, player):
		num = random.randint(0, len(card_test.chestcards))
		print(card_test.chestcards[num])
		if num == 0:
			player[0].position = 0
			player[0].money = player[0].money + 200
		elif num == 1:
			player[0].money = player[0].money + 200
		elif num == 2:
			player[0].money = player[0].money - 50
		elif num == 3:
			player[0].money = player[0].money + 50
		elif num == 4:
			player[0].in_jail = True
			player[0].position = 10
		elif num == 5:
			player[0].money = player[0].money + 100
		elif num == 6:
			player[0].money = player[0].money + 20
		elif num == 7:
			for plr in self.players:
				if plr != player and plr[0].eliminated == False:
					plr[0].money = plr[0].money - 10
					player[0].money = player[0].money + 10
		elif num == 8:
			player[0].money = player[0].money + 100
		elif num == 9:
			player[0].money = player[0].money - 100
		elif num == 10:
			player[0].money = player[0].money - 50
		elif num == 11:
			player[0].money = player[0].money - 25
		elif num == 12:
			fee = 0
			for tile in self.tiles:
				if tile[0].tile_type == "PropertyTile" and tile[0].owner == player:
					if tile[0].house_count == 5:
						fee = fee + 115
					else:
						fee = fee + tile[0].house_count*40
			player[0].money = player[0].money - fee
		elif num == 13:
			player[0].money = player[0].money + 10
		elif num == 14:
			player[0].money = player[0].money + 100

	def draw_chance(self, player):
		num = random.randint(0, len(card_test.chancecards))
		print(card_test.chancecards[num])
		if num == 0:
			player[0].position = 39
		elif num == 1:
			player[0].position = 0
			player[0].money = player[0].money + 200
		elif num == 2:
			if player[0].position > 24:
				player[0].money = player[0].money + 200
			player[0].position = 24
		elif num == 3:
			if player[0].position > 11:
				player[0].money = player[0].money + 200
			player[0].position = 11
		elif num == 4:
			shortest_distance = 50
			assoc_tile = None
			for tile in self.tiles:
				if tile[0].tile_type == "RailroadTile":
					new_distance = abs(player[0].position - tile[0].tile_id)
					if new_distance < shortest_distance:
						shortest_distance = new_distance
						assoc_tile = tile
			player[0].position = assoc_tile[0].tile_id
		elif num == 5:
			shortest_distance = 50
			assoc_tile = None
			for tile in self.tiles:
				if tile[0].tile_type == "UtilityTile":
					new_distance = abs(player[0].position - tile[0].tile_id)
					if new_distance < shortest_distance:
						shortest_distance = new_distance
						assoc_tile = tile
			player[0].position = assoc_tile[0].tile_id
		elif num == 6:
			player[0].money = player[0].money + 50
		elif num == 7:
			new_position = player[0].position - 3
			if new_position < 0:
				player[0].position = new_position + 40
			else:
				player[0].position = new_position
		elif num == 8:
			player[0].in_jail = True
			player[0].position = 10
		elif num == 9:
			fee = 0
			for tile in self.tiles:
				if tile[0].tile_type == "PropertyTile" and tile[0].owner == player:
					if tile[0].house_count == 5:
						fee = fee + 100
					else:
						fee = fee + tile[0].house_count*35
			player[0].money = player[0].money - fee
		elif num == 10:
			player[0].money = player[0].money - 15
		elif num == 11:
			if player[0].position > 5:
				player[0].money = player[0].money + 200
			player[0].position = 5
		elif num == 12:
			for plr in self.players:
				if plr != player and plr[0].eliminated == False:
					plr[0].money = plr[0].money + 50
					player[0].money = player[0].money - 50
		elif num == 13:
			player[0].money = player[0].money + 150

	def to_jail(self, player):
		player[0].in_jail = True
		player[0].position = 10

	def has_monopoly(self, player, color):
		validity = True
		for prop in self.tiles:
			if (prop[0].tile_type == "PropertyTile") and prop[0].color == color:
				if prop[0].owner != player:
					validity = False
		return validity

	def railroads_owned(self, player):
		railroads = 0
		for prop in self.tiles:
			if (prop[0].tile_type == "RailroadTile") and prop[0].owner == player:
				railroads = railroads + 1
		return railroads

	def utilities_owned(self, player):
		utilities = 0
		for prop in self.tiles:
			if (prop[0].tile_type == "UtilityTile") and prop[0].owner == player:
				utilities = utilities + 1
		return utilities

	def get_player(self, player_name):
		for plr in self.players:
			if plr[0].name == player_name:
				return plr

	def buy_property(self, player, property):
		if player[0].money >= property[0].cost:
			player[0].money = player[0].money - property[0].cost
			property[0].owner = player

	def sell_property(self, player, property):
		if self.has_monopoly(player, property[0].color): # will cancel monopoly. must sell all other houses
			for prop in self.tiles:
				if prop[0].tile_type == "PropertyTile" and prop[0].color == property[0].color:
					player[0].money = player[0].money + (self.mortgage_rate * prop[0].house_price * prop[0].house_count)
					prop[0].house_count = 0
		player[0].money = player[0].money + (self.mortgage_rate * property[0].cost)
		property[0].owner = None

	def buy_house(self, player, property):
		if player[0].money >= property[0].house_price and self.has_monopoly(player, property[0].color):
			property[0].house_count = property[0].house_count + 1
			player[0].money = player[0].money - property[0].house_price

	def sell_house(self, player, property):
		player[0].money = player[0].money + (property[0].house_price * self.mortgage_rate)
		property[0].house_count = property[0].house_count - 1

	def roll_dice(self, player):
		#roll1 = random.randint(1, 6)
		#roll2 = random.randint(1, 6)
		roll1 = 1
		roll2 = 1
		total_roll = roll1 + roll2
		if player[0].in_jail == True:
			if roll1 == roll2:
				player[0].in_jail = False
			else:
				return False

		initial_pos = player[0].position
		new_pos = initial_pos + total_roll

		if new_pos >= 40:	# passing go, collect 200
			new_pos = new_pos - 40
			player[0].money = player[0].money + 200

		player[0].position = new_pos
		landed_on = self.tiles[new_pos]

		#print("Rolled " + roll1 + " & " + roll2 + ", went from " + self.tiles[initial_pos].name + " to " + landed_on[0].name)
		print("Rolled {0} & {1}, went from '{2}' to '{3}'".format(roll1, roll2, self.tiles[initial_pos][0].name, landed_on[0].name))

		if landed_on[0].tile_type == "PropertyTile" or landed_on[0].tile_type == "RailroadTile" or landed_on[0].tile_type == "UtilityTile":
			if landed_on[0].owner == None:
				if player[0].money >= landed_on[0].cost:
					# give player choice to buy. call self.buy_property(player, landed_on) if they want to buy it
					self.buy_property(player, landed_on)
					print("Purchased {0} for ${1}, now at ${2}".format(landed_on[0].name, landed_on[0].cost, player[0].money))
			elif landed_on[0].owner != player:
				# pay rent
				rent_cost = 0
				if landed_on[0].tile_type == "PropertyTile":
					num_houses = landed_on[0].house_count
					if num_houses == 0 and self.has_monopoly(landed_on[0].owner, landed_on[0].color):
						rent_cost = landed_on[0].penalties[0] * self.monopoly_rate
					else:
						rent_cost = landed_on[0].penalties[num_houses]
				elif landed_on[0].tile_type == "RailroadTile":
					railroads = self.railroads_owned(landed_on[0].owner)
					rent_cost = self.railroad_rate[railroads-1]
				elif landed_on[0].tile_type == "UtilityTile":
					utilities = self.utilities_owned(landed_on[0].owner)
					if utilities == 1:
						rent_cost = total_roll * 4
					elif utilities == 2:
						rent_cost = total_roll * 10

				if player[0].money - rent_cost < 0:
					landed_on[0].owner[0].money = landed_on[0].owner[0].money + player[0].money
				else:
					landed_on[0].owner[0].money = landed_on[0].owner[0].money + rent_cost

				player[0].money = player[0].money - rent_cost
				print("Paid ${0} of rent to {1}".format(rent_cost, landed_on[0].owner[0].name))
		elif landed_on[0].tile_type == "TaxTile":
			rent_cost = landed_on[0].penalty
			player[0].money = player[0].money - rent_cost
			print("Paid ${0} of tax".format(rent_cost))
		elif landed_on[0].tile_type == "CornerTile" and landed_on[0].sends_to_prison == True:
			self.to_jail(player)
		elif landed_on[0].tile_type == "CardTile":
			if landed_on[0].name == "Comm Chest":
				self.draw_chest(player)
			elif landed_on[0].name == "Chance":
				self.draw_chance(player)
		
		if roll1 == roll2: # code that calls this will use it to determine whether or not they get to immediately roll again
			return True	   # be sure to make it so rolling doubles 3 times in a row will put you in jail
		else:
			return False

game = Board()
game.initialize()
game.add_player("Player 1")
game.add_player("Player 2")

def draw_buttons():
	# Load button images and rotate them
	commtest = pygame.image.load('assets/comm_test.png').convert_alpha()
	commtest = pygame.transform.rotate(commtest, 45)
	commtest.set_colorkey((0, 0, 0)) # sets black as the transparent color
	chancetest = pygame.image.load('assets/chance_test.png').convert_alpha()
	chancetest = pygame.transform.rotate(chancetest, 45)
	chancetest.set_colorkey((0, 0, 0)) # sets black as the transparent color

	# Blit button images to the screen
	screen.blit(commtest, (commbutton.x, commbutton.y))
	screen.blit(chancetest, (chancebutton.x, chancebutton.y))

	# Draw button rectangles to see where buttons are
	pygame.draw.rect(screen, (255, 0, 0), commbutton, -1)
	pygame.draw.rect(screen, (255, 0, 0), chancebutton, -1)

for i in range(40):
	tile = game.tiles[i]
	tile[0].tile_id = i
	if i >= 0 and i < 10:
		xpos = width*(i/11)
		ypos = height*0
	elif i >= 10 and i < 20:
		xpos = width*(10/11)
		ypos = height*(i-10)/11
	elif i >= 20 and i < 30:
		xpos = width*(10-(i-20))/11
		ypos = height*(10/11)
	elif i >= 30 and i < 40:
		xpos = width*0
		ypos = height*(10-(i-30))/11
	
	tile[0].outline = pygame.Rect(xpos, ypos, width/11, width/11)
	tile[0].name_text = font.render(tile[0].name, True, (0, 0, 0))

	if tile[0].tile_type == "PropertyTile":
		if tile[0].color == "Brown":
			banner_color = (112, 74, 20)
		elif tile[0].color == "Cyan":
			banner_color = (56, 255, 248)
		elif tile[0].color == "Pink":
			banner_color = (255, 0, 208)
		elif tile[0].color == "Orange":
			banner_color = (255, 111, 0)
		elif tile[0].color == "Red":
			banner_color = (255, 0, 0)
		elif tile[0].color == "Yellow":
			banner_color = (251, 255, 0)
		elif tile[0].color == "Green":
			banner_color = (0, 135, 7)
		elif tile[0].color == "Blue":
			banner_color = (4, 0, 255)
		
		tile[0].banner = pygame.Rect(xpos, ypos, width/11, width/11/4)
		tile[0].banner_c = banner_color
		tile[0].cost_text = font.render("$" + str(tile[0].cost), True, (0, 0, 0))

		squares = []
		for j in range(4):
			squares.append(pygame.Rect(xpos, ypos+width/11/4+(width/11*(3/4)/4)*j, width/11*(3/4)/4, width/11*(3/4)/4))
		tile[0].house_squares = squares
	elif tile[0].tile_type == "RailroadTile":
		tile[0].cost_text = font.render("$" + str(tile[0].cost), True, (0, 0, 0))
	elif tile[0].tile_type == "TaxTile":
		tile[0].tax_text = font.render("$" + str(tile[0].penalty), True, (0, 0, 0))

def draw_board():
	# Load the board image and scale it to the size of the screen
	boardImg = pygame.image.load('assets/board.png')
	boardImg = pygame.transform.scale(boardImg, (width, height))
	screen.blit(boardImg, (0, 0)) # Blit the board image onto the screen

	for i in range(40):
		tile = game.tiles[i]
		tile[0].draw()

	for player in game.players:
		tile = game.tiles[player[0].position]

		if player == game.players[0]:
			player_piece = pygame.Rect(tile[0].outline.x+(width/11)*0.228125, tile[0].outline.y+(width/11)/4+5, (width/11)*0.73125, 15)
		else:
			player_piece = pygame.Rect(tile[0].outline.x+(width/11)*0.228125, tile[0].outline.y+(width/11)/4+25, (width/11)*0.73125, 15)
		pygame.draw.rect(screen, (0, 0, 0), player_piece, 0)

		player_text = font.render(player[0].name, True, (255, 255, 255))
		screen.blit(player_text, (player_piece.x, player_piece.y))

pygame.display.update()

# this is just testing stuff below
#game.roll_dice(game.players[0])
#game.roll_dice(game.players[1])
game.buy_property(game.players[0], game.tiles[37])
print(game.players[0][0].money)
game.buy_property(game.players[0], game.tiles[39])
print(game.players[0][0].money)
game.buy_house(game.players[0], game.tiles[39])
print(game.players[0][0].money)
game.buy_house(game.players[0], game.tiles[39])
game.buy_house(game.players[0], game.tiles[39])
game.buy_house(game.players[0], game.tiles[39])
game.buy_house(game.players[0], game.tiles[39])
game.buy_house(game.players[0], game.tiles[39])
game.sell_house(game.players[0], game.tiles[39])

print(game.players[0][0].money)
print(game.tiles[39][0].house_count)
#game.sell_property(game.players[0], game.tiles[39])
#print(game.players[0][0].money)
game.roll_dice(game.players[0])

i = 1
frame_count = 0
while running:

	# Define font and text
	prompt_font = pygame.font.Font(None, 32)
	prompt_text = prompt_font.render("Do you want to roll the dice? (Y/N)", True, (255, 255, 255))

	# Get position of text on screen
	text_rect = prompt_text.get_rect()
	text_rect.center = (width / 2, height / 2)

	# Blit text to screen
	screen.blit(prompt_text, text_rect)

	# Display "Yes" and "No" buttons
	yes_button = pygame.Rect(width/3, height/2+50, 100, 50)
	no_button = pygame.Rect(2*width/3, height/2+50, 100, 50)
	pygame.draw.rect(screen, (0, 255, 0), yes_button)
	pygame.draw.rect(screen, (255, 0, 0), no_button)
	yes_text = font.render("Yes", True, (255, 255, 255))
	yes_text_rect = yes_text.get_rect(center=yes_button.center)
	screen.blit(yes_text, yes_text_rect)
	no_text = font.render("No", True, (255, 255, 255))
	no_text_rect = no_text.get_rect(center=no_button.center)
	screen.blit(no_text, no_text_rect)




	pygame.display.flip()  # refresh screen
	clock.tick(60)         # wait until next frame (60 fps)
	current_time = pygame.time.get_ticks()

	# draw board each frame
	draw_board()

	#draw buttons each frame
	draw_buttons()
	
	#event checker
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

		# putting in card draw test stuff
		# draw from chance
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:           
			if chancebutton.collidepoint(pygame.mouse.get_pos()):
				pass
				#drawn = card_test.draw_card("chance")
				#text = font.render(drawn, True, (155,0,0))
				#message_end_time = pygame.time.get_ticks() + 2000

		# draw from community chest
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:           
			if commbutton.collidepoint(pygame.mouse.get_pos()):
				pass
				#drawn = card_test.draw_card("chest")
				#text = font.render(drawn, True, (0,0,155))
				#message_end_time = pygame.time.get_ticks() + 2000

	#display message for set amt of time
	if current_time < message_end_time:
		screen.blit(text, text.get_rect(center = screen.get_rect().center))
	
	if frame_count <= 1:
		game.roll_dice(game.players[0])
		#pass

	pygame.display.flip()
	frame_count = frame_count + 1

pygame.quit()
