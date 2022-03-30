import pygame as pg

# загрузка всех текстур
Textures = {
	'BAKE': pg.image.load(F'bake.png'),
	'CASE_OPEN': pg.image.load(F'case_open.png'),
	'CASE_CLOSE': pg.image.load(F'case_close.png'),
	'DOOR':pg.image.load(F'door.png'),
	'STAIRS':pg.image.load(F'stairs.png'),
	'PLATFORM':pg.image.load(F'platform.png')
}
nothing_image = pg.image.load(F'nothing.png')

# класс текстур
class Texture(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

# класс блоков
class Block(pg.sprite.Sprite):
	def __init__(self, image_file, location, name):
		pg.sprite.Sprite.__init__(self)
		self.image = image_file
		self.rect = self.image.get_rect()
		self.local = location
		self.rect.left, self.rect.top = location
		self.name = name

# класс выбора блока
class Selected(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

# класс персонажа
class Person(pg.sprite.Sprite):
	def __init__(self, location):
		pg.sprite.Sprite.__init__(self)
		self.image_right_idle = pg.image.load(F'person_right_idle.png')
		self.image_left_idle = pg.image.load(F'person_left_idle.png')
		self.image_idle = self.image_right_idle
		self.image_right_fall = pg.image.load(F'person_right_fall.png')
		self.image_left_fall = pg.image.load(F'person_left_fall.png')
		self.image_fall = self.image_right_fall
	# загрузка кадров ходьбы
		self.image_walk_right = []
		self.image_walk_right.append(pg.image.load(F'person_right_step_1.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_2.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_3.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_4.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_5.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_6.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_7.png'))
		self.image_walk_right.append(pg.image.load(F'person_right_step_8.png'))
		self.image_walk_left = []
		self.image_walk_left.append(pg.image.load(F'person_left_step_1.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_2.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_3.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_4.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_5.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_6.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_7.png'))
		self.image_walk_left.append(pg.image.load(F'person_left_step_8.png'))
	#
		self.image = self.image_idle
		self.rect = self.image.get_rect()
		self.local = location
		self.rect.left, self.rect.top = location
		self.helth = 100
		self.speed = 5
		self.step_num = 0
		self.moving_left = False
		self.moving_right = False
		self.fall = False
		self.jump = False
		self.amount_grass = 0
		self.amount_earth = 0
		self.amount_boards = 0
		self.amount_tree = 0
		self.amount_stone = 0
		self.amount_bake = 0
		self.amount_case = 0
		self.amount_stairs = 0
		self.amount_platform = 0
		self.amount_door = 0
		self.amount_sugar = 0

	def GetItem(self, item_type, amount_item):
		if item_type == 'board':
			self.amount_boards += amount_item
		elif item_type == 'grass':
			self.amount_grass += amount_item
		elif item_type == 'earth':
			self.amount_earth += amount_item
		elif item_type == 'tree':
			self.amount_tree += amount_item
		elif item_type == 'stone':
			self.amount_stone += amount_item
		elif item_type == 'bake':
			self.amount_bake += amount_item
		elif item_type == 'case':
			self.amount_case += amount_item
		elif item_type == 'stairs':
			self.amount_stairs += amount_item
		elif item_type == 'platform':
			self.amount_platform += amount_item
		elif item_type == 'door':
			self.amount_door += amount_item
		elif item_type == 'sugar':
			self.amount_sugar += amount_item

	def UPDATE(self):
		if self.moving_right:
			self.rect.left += self.speed
		if self.moving_left:
			self.rect.left -= self.speed
		if self.jump:
			self.rect.top -= 5
		elif self.fall:
			self.image = self.image_fall
			self.rect.top += 5
		else:
			self.image = self.image_idle
		if self.rect.left > 791:
			self.rect.left = 5
			self.rect.top -= 20
		elif self.rect.left < 4:
			self.rect.left = 790
			self.rect.top -= 20
		if self.moving_right:
			if self.step_num < 3:
				self.image = self.image_walk_right[0]
				self.step_num +=1
			elif self.step_num < 6:
				self.image = self.image_walk_right[1]
				self.step_num +=1
			elif self.step_num < 9:
				self.image = self.image_walk_right[2]
				self.step_num +=1
			elif self.step_num < 12:
				self.image = self.image_walk_right[3]
				self.step_num +=1
			elif self.step_num < 15:
				self.image = self.image_walk_right[4]
				self.step_num +=1
			elif self.step_num < 18:
				self.image = self.image_walk_right[5]
				self.step_num +=1
			elif self.step_num < 21:
				self.image = self.image_walk_right[6]
				self.step_num +=1
			elif self.step_num < 24:
				self.image = self.image_walk_right[7]
				self.step_num +=1 
			else:
				self.step_num = 0
		if self.moving_left:
			if self.step_num < 3:
				self.image = self.image_walk_left[0]
				self.step_num +=1
			elif self.step_num < 6:
				self.image = self.image_walk_left[1]
				self.step_num +=1
			elif self.step_num < 9:
				self.image = self.image_walk_left[2]
				self.step_num +=1
			elif self.step_num < 12:
				self.image = self.image_walk_left[3]
				self.step_num +=1
			elif self.step_num < 15:
				self.image = self.image_walk_left[4]
				self.step_num +=1
			elif self.step_num < 18:
				self.image = self.image_walk_left[5]
				self.step_num +=1
			elif self.step_num < 21:
				self.image = self.image_walk_left[6]
				self.step_num +=1
			elif self.step_num < 24:
				self.image = self.image_walk_left[7]
				self.step_num +=1 
			else:
				self.step_num = 0

# класс инвентаря 
class Inventory(pg.sprite.Sprite):
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.selected_item = 0
		self.items = []
		for x in range(0,24):
			self.items.append(0)

# класс быстрого меню
class FastInventory():
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.selected_item = 0
		self.items = []
		for x in range(0,3):
			self.items.append(0)

# класс крафта 
class Craft(pg.sprite.Sprite):
	def __init__(self, location):
		pg.sprite.Sprite.__init__(self)
		self.image_button = pg.image.load(F'craft_button.png')
		self.image_craft = pg.image.load(F'craft.png')
		self.image = self.image_button
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.selected_item = 0

# класс инвентаря 
class Case(pg.sprite.Sprite):
	def __init__(self, location, name):
		pg.sprite.Sprite.__init__(self)
		self.image_open = Textures['CASE_OPEN']
		self.image_close = Textures['CASE_CLOSE']
		self.image = self.image_close
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.selected_item = 0
		self.name = name
		self.open = False
		self.items = []
		for x in range(0,24):
			self.items.append(0)

	def Open(self):
			self.image = self.image_open
			self.rect.top -= 5
			self.open = True

	def Close(self):
			self.image = self.image_close
			self.rect.top += 5
			self.open = False
