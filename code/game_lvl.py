import pygame as pg
import math as mt
import classes as cl
import random

# инициализация pg
pg.init()

# ширина и высота окна
WIDTH, HEIGHT = 800, 600

# объявление штук pg 
sc = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# загрузка всех текстур
Textures = {
	'GRASS': pg.image.load(F'grass.jpg'),
	'EARTH': pg.image.load(F'earth.jpg'),
	'BOARDS': pg.image.load(F'boards.jpg'),
	'TREE': pg.image.load(F'tree.jpg'),
	'STONE': pg.image.load(F'stone.jpg'),
	'LEAVES_1': pg.image.load(F'leaves_1.png'),
	'LEAVES_2': pg.image.load(F'leaves_2.png'),
	'BAKE': pg.image.load(F'bake.png'),
	'CASE': pg.image.load(F'case_close.png'),
	'SUGAR': pg.image.load(F'sugar.png'),
	'DOOR':pg.image.load(F'door.png'),
	'STAIRS':pg.image.load(F'stairs.png'),
	'PLATFORM':pg.image.load(F'platform.png')
}

# ограничение по fps
FPS = 60

# ограничение высоты прыжка
delta_jump = 0

# кароч ходьба блять
step_num = 0

# указатель на выбранный блок
selection = cl.Selected(
	F'selection.png',
	[400, 400])
selection_item = cl.Selected(
	F'selected_item.png',
	[20, 20])
selection_item.num_sel = 1
selection_inventory = cl.Selected(
	F'selected_item.png',
	[219, 25])

selection_craft = cl.Selected(
	F'selected_item.png',
	[415, 20])


# быстрыя инвентарь
fast_inventory = cl.FastInventory(
	F'fast_inventory.png',
	[20, 20])

# создание инвенторя
inventory = cl.Inventory(
	F'inventory.png',
	[214, 20])
show_inventory = False

# кнопка выхода из игры
game_exit = cl.Texture(F'exit_menu.png', [565, 20])

# вывод названия объкта
f1 = pg.font.Font(None, 20)
item_name = f1.render('пусто', True, (255, 255, 255))
try:
	inventory_item_name = f1.render('блок: ' + str(len(inventory.items[inventory.selected_item]) + 1), True, (255, 255, 255))
except TypeError:
	inventory_item_name = f1.render('пусто', True, (255, 255, 255))

# создание персонажа
person = cl.Person([400, 300])

# счетчик урона
person_damage = 0

# количество жизней персонажа
person_helth = f1.render('НР: ' + str(person.helth), True, (255, 255, 255))

# создание заднего фона
background = cl.Texture(
	F'background.jpg',
	[0, 0])

#
blocks = []
for x in range(0,40):
	blocks.append(cl.Block(
		Textures['GRASS'],
		[20 * x, 400],
		'grass'))
	for y in range(21,25):
		blocks.append(cl.Block(
			Textures['EARTH'],
			[20 * x, 20 * y],
			'earth'))
	for y in range(25,30):
		blocks.append(cl.Block(
			Textures['STONE'],
			[20 * x, 20 * y],
			'stone'))

trees = []
leaves = []
tree_x = set()
for x in range(0, 6):
	tree_x.add(random.randint(20, 780)//20)
for tr in tree_x:
	for y in range(0, random.randint(3, 15)):
		trees.append(cl.Block(
			Textures['TREE'],
			[20 * tr, 380 - 20 * y],
			'tree'))
	if trees[-1].rect.top >= 280:
		leaves.append(cl.Block(
			Textures['LEAVES_1'],
			[trees[-1].rect.left - 20, trees[-1].rect.top - 40],
			'leaves'))
	else:
		leaves.append(cl.Block(
			Textures['LEAVES_2'],
			[trees[-1].rect.left - 20, trees[-1].rect.top - 40],
			'leaves'))

# создание досок
boards = []

# создание крафта
craft = cl.Craft([415, 20])

# создание фурнитуры
furniture = []

# создание платформ
platforms = []

# создание сундуков
cases = []

# добавление стартовых блоков
def AddHelpBlock():
	# добавление тестовых досок в инвентарь
	board = []
	for x in range(1,10):
		board.append(cl.Block(Textures['BOARDS'], [225, 30], 'board'))
	inventory.items.insert(0, board)
	
	# добавление тестово земли в инвентарь
	grass = []
	for x in range(1,10):
		grass.append(cl.Block(Textures['EARTH'], [256, 30], 'earth'))
	inventory.items.insert(1, grass)
	
	# добавление тестово травы в инвентарь
	bard = []
	for x in range(1,10):
		bard.append(cl.Block(Textures['GRASS'], [287, 30], 'grass'))
	inventory.items.insert(2, bard)

	rock = []
	for x in range(1,10):
		rock.append(cl.Block(Textures['STONE'], [318, 30], 'stone'))
	inventory.items.insert(3, rock)
	
	tree = []
	for x in range(1,10):
		tree.append(cl.Case([349, 30], 'case'))
	inventory.items.insert(4, tree)	

# поиск нужных ресурсов
def SearchResourses(name_resourse):
	for sel in inventory.items:
		try:
			if sel[0].name == name_resourse:
				sel.pop(-1)
				return len(sel) + 1
		except TypeError:
			continue
		except IndexError:
			continue
	return 0

# упорядочивание в инвентаре
def SortInventoryItems():
	for sel in range(0, 6):
		try:
			for blo in inventory.items[sel]:
				blo.rect.left = 225 + 31 * sel
				blo.rect.top = 30
				inventory_item_name = f1.render(blo.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
					True, (255, 255, 255))
				break
		except TypeError:
			inventory_item_name = f1.render('пусто', True, (255, 255, 255))
	for sel in range(6, 12):
		try:
			for blo in inventory.items[sel]:
				blo.rect.left = 225 + 31 * (sel - 6)
				blo.rect.top = 61
				inventory_item_name = f1.render(blo.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
					True, (255, 255, 255))
				break
		except TypeError:
			inventory_item_name = f1.render('пусто', True, (255, 255, 255))
	for sel in range(12, 18):
		try:
			for blo in inventory.items[sel]:
				blo.rect.left = 225 + 31 * (sel - 12)
				blo.rect.top = 92
				inventory_item_name = f1.render(blo.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
					True, (255, 255, 255))
				break
		except TypeError:
			inventory_item_name = f1.render('пусто', True, (255, 255, 255))
	for sel in range(18, 24):
		try:
			for blo in inventory.items[sel]:
				blo.rect.left = 225 + 31 * (sel - 18)
				blo.rect.top = 123
				inventory_item_name = f1.render(blo.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
					True, (255, 255, 255))
				break
		except TypeError:
			inventory_item_name = f1.render('пусто', True, (255, 255, 255))

# добавить в инвентарь новый блок
def AddBlock(item):
	ind = True
	for it in inventory.items:
		try:
			if it[0].name == item.name:
				it.append(item)
				ind = False
				break
		except TypeError:
			pass
		except IndexError:
			pass
	if ind:
		black = []
		black.append(item)
		inventory.items.insert(inventory.items.index(0), black)
		SortInventoryItems()

# при ломании блока
def BreakBlock(items):
	for bl in items:
		if bl.rect.collidepoint(
			selection.rect.left + 10, 
			selection.rect.top + 10):
			person.GetItem(bl.name, 1)
			ind = True
			for it in inventory.items:
				try:
					if it[0].name == bl.name:
						it.append(bl)
						ind = False
						break
				except TypeError:
					pass
				except IndexError:
					pass
			if ind:
				black = []
				black.append(bl)
				inventory.items.insert(inventory.items.index(0), black)
				inventory.items.remove(0)
				SortInventoryItems()
			items.remove(bl)

# обработка выбора в быстром инвентаре
def SelectInFastInventory(num):
	if num == 0:
		selection_item.rect.left = 20
	elif num == 1:
		selection_item.rect.left = 52
	elif num == 2:
		selection_item.rect.left = 84
	fast_inventory.selected_item = num
	selection_item.num_sel = num
	try:
		for bl in fast_inventory.items[fast_inventory.selected_item]:
			return f1.render(bl.name + ': ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
				True, (255, 255, 255))
			break
	except TypeError:
		return f1.render('пусто', True, (255, 255, 255))

# главный цикл
def Game(cheat):

	if cheat:
		AddHelpBlock()
	item_name = f1.render('пусто', True, (255, 255, 255))
	show_inventory = False
	try:
		inventory_item_name = f1.render(inventory.items[inventory.selected_item][0].name + ': ' + str(len(inventory.items[inventory.selected_item]) + 1), 
			True, (255, 255, 255))
	except TypeError:
		inventory_item_name = f1.render('пусто', True, (255, 255, 255))
	except IndexError:
		inventory_item_name = f1.render('пусто', True, (255, 255, 255))

	show_craft = False

	person.helth = 100

	frame = 0

	while True:
		frame += 1
		if frame % 7200 == 0 and frame != 0:
			person.helth -= 10
			if person.helth == 0:
				inventory.items.clear()
				fast_inventory.items.clear()
				return

		for event in pg.event.get():
			if event.type == pg.QUIT:
				return
# обработка действий с мыши
			elif event.type == pg.MOUSEBUTTONDOWN:
				mouse_pos = event.pos  
			
				if game_exit.rect.collidepoint(mouse_pos):
					return 
# обработка действий с клавиатуры
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					return
				elif event.key == pg.K_d:
					person.image_idle = person.image_right_idle
					person.image_fall = person.image_right_fall
					person.moving_right = True
				elif event.key == pg.K_a:
					person.image_idle = person.image_left_idle
					person.image_fall = person.image_left_fall
					person.moving_left = True
				elif event.key == pg.K_SPACE:
					person.jump = True
				elif event.key == pg.K_RIGHT:
					if show_inventory:
						if selection_inventory.rect.left < 370:
							selection_inventory.rect.left += 31
							inventory.selected_item += 1
						try:
							for bl in inventory.items[inventory.selected_item]:
								inventory_item_name = f1.render(bl.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
									True, (255, 255, 255))
								break
						except TypeError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
					else:
						selection.rect.left += 20
				elif event.key == pg.K_LEFT:
					if show_inventory:
						if selection_inventory.rect.left > 225:
							selection_inventory.rect.left -= 31
							inventory.selected_item -= 1
						try:
							for bl in inventory.items[inventory.selected_item]:
								inventory_item_name = f1.render(bl.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
									True, (255, 255, 255))
								break
						except TypeError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
					else:
						selection.rect.left -= 20
				elif event.key == pg.K_UP:
					if show_inventory:
						if selection_inventory.rect.top > 25:
							selection_inventory.rect.top -= 31
							inventory.selected_item -= 6
						try:
							for bl in inventory.items[inventory.selected_item]:
								inventory_item_name = f1.render(bl.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
									True, (255, 255, 255))
								break
						except TypeError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
					else:
						selection.rect.top -= 20
				elif event.key == pg.K_DOWN:
					if show_inventory:
						if selection_inventory.rect.top < 100:
							selection_inventory.rect.top += 31
							inventory.selected_item += 6
						try:
							for bl in inventory.items[inventory.selected_item]:
								inventory_item_name = f1.render(bl.name + ': ' + str(len(inventory.items[inventory.selected_item])), 
									True, (255, 255, 255))
								break
						except TypeError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
					else:
						selection.rect.top += 20
			# удаление блоков
				elif event.key == pg.K_r:
					if mt.sqrt(abs((person.rect.left + 10) - (selection.rect.left + 10)) ** 2 + 
						abs((person.rect.top + 20) - (selection.rect.top + 10)) ** 2) <= 100:
						if selection_item.num_sel == 4:
							BreakBlock(blocks)
						elif selection_item.num_sel == 6:
							BreakBlock(boards)
							BreakBlock(trees)
			# постройка блоков
				elif event.key == pg.K_e:
					if (mt.sqrt(abs((person.rect.left + 10) - (selection.rect.left + 10)) ** 2 + 
							abs((person.rect.top + 20) - (selection.rect.top + 10)) ** 2) <= 100 and 
						selection_item.num_sel < 3):
						try:
							if (fast_inventory.items[fast_inventory.selected_item][0].name == 'grass' and 
								person.amount_grass > 0):
								blocks.append(cl.Block(
									Textures['GRASS'],
									[selection.rect.left, selection.rect.top],
									'grass'))
								person.amount_grass -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('grass: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'earth' and 
								person.amount_earth > 0):
								blocks.append(cl.Block(
									Textures['EARTH'],
									[selection.rect.left, selection.rect.top],
									'earth'))
								person.amount_earth -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('earth: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'board' and 
								person.amount_boards > 0):
								boards.append(cl.Block(
									Textures['BOARDS'],
									[selection.rect.left, selection.rect.top],
									'board'))
								person.amount_boards -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('board: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'tree' and 
								person.amount_tree > 0):
								boards.append(cl.Block(
									Textures['TREE'],
									[selection.rect.left, selection.rect.top],
									'tree'))
								person.amount_tree -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('tree: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'stone' and 
								person.amount_stone > 0):
								blocks.append(cl.Block(
									Textures['STONE'],
									[selection.rect.left, selection.rect.top],
									'stone'))
								person.amount_stone -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('stone: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'bake' and 
								person.amount_bake > 0):
								furniture.append(cl.Block(
									Textures['BAKE'],
									[selection.rect.left, selection.rect.top],
									'bake'))
								person.amount_bake -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('bake: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'door' and 
								person.amount_door > 0):
								furniture.append(cl.Block(
									Textures['DOOR'],
									[selection.rect.left, selection.rect.top],
									'door'))
								person.amount_stone -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('door: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'case' and 
								person.amount_case > 0):
								case = cl.Case(
									[selection.rect.left, selection.rect.top],
									'case')
								case.Close()
								cases.append(case)
								person.amount_case -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('case: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'stairs' and 
								person.amount_stairs > 0):
								furniture.append(cl.Block(
									Textures['STAIRS'],
									[selection.rect.left, selection.rect.top],
									'stairs'))
								person.amount_stairs -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('stairs: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
							elif (fast_inventory.items[fast_inventory.selected_item][0].name == 'platform' and 
								person.amount_platform > 0):
								platforms.append(cl.Block(
									Textures['PLATFORM'],
									[selection.rect.left, selection.rect.top],
									'platform'))
								person.amount_platform -= 1
								fast_inventory.items[fast_inventory.selected_item].pop(0)
								item_name = f1.render('platform: ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
									True, (255, 255, 255))
						except TypeError:
							pass
						except IndexError:
							pass
			# управление быстрым инвентарем
				elif event.key == pg.K_1:
					item_name = SelectInFastInventory(0)
					selection_item.num_sel = 0
				elif event.key == pg.K_2:
					item_name = SelectInFastInventory(1)
					selection_item.num_sel = 0
				elif event.key == pg.K_3:
					item_name = SelectInFastInventory(2)
					selection_item.num_sel = 0
				elif event.key == pg.K_4:
					selection_item.rect.left = 116
					selection_item.num_sel = 4
					item_name = f1.render('кирка', True, (255, 255, 255))
				elif event.key == pg.K_5:
					selection_item.rect.left = 148
					selection_item.num_sel = 5
					item_name = f1.render('мечь', True, (255, 255, 255))
				elif event.key == pg.K_6:
					selection_item.rect.left = 180
					selection_item.num_sel = 6
					item_name = f1.render('топор', True, (255, 255, 255))
				elif event.key == pg.K_TAB:
					if show_inventory:
						show_inventory = False
						show_craft = False
						craft.image = craft.image_button
					else:
						show_inventory = True
					try:
						inventory_item_name = f1.render(inventory.items[inventory.selected_item][0].name + ': ' + str(len(inventory.items[inventory.selected_item])),
						True, (255, 255, 255))
					except TypeError:
						inventory_item_name = f1.render('пусто', True, (255, 255, 255))
					except IndexError:
						inventory_item_name = f1.render('пусто', True, (255, 255, 255))
				elif event.key == pg.K_q:
					if show_inventory:
						fast_inventory.items[fast_inventory.selected_item], inventory.items[inventory.selected_item] = inventory.items[inventory.selected_item], fast_inventory.items[fast_inventory.selected_item]
						try:
							person.GetItem(fast_inventory.items[fast_inventory.selected_item][0].name, 
								len(fast_inventory.items[fast_inventory.selected_item]))
						except TypeError:
							pass
						except IndexError:
							pass
						try:
							person.GetItem(inventory.items[inventory.selected_item][0].name, 
								(len(inventory.items[inventory.selected_item])) * -1)
						except TypeError:
							pass 
						except IndexError:
							pass
						SortInventoryItems()
						try:
							inventory_item_name = f1.render(inventory.items[inventory.selected_item][0].name + ': ' + str(len(inventory.items[inventory.selected_item])), 
								True, (255, 255, 255))
						except TypeError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
						except IndexError:
							inventory_item_name = f1.render('пусто', True, (255, 255, 255))
						if fast_inventory.selected_item == 0:
							try:
								for bl in fast_inventory.items[fast_inventory.selected_item]:
									bl.rect.left = 25
									bl.rect.top = 25
									item_name = f1.render(bl.name + ': ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
										True, (255, 255, 255))
							except TypeError:
								item_name = f1.render('пусто', True, (255, 255, 255))
						elif fast_inventory.selected_item == 1:
							try:
								for bl in fast_inventory.items[fast_inventory.selected_item]:
									bl.rect.left = 57
									bl.rect.top = 25
									item_name = f1.render(bl.name + ': ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
										True, (255, 255, 255))
							except TypeError:
								item_name = f1.render('пусто', True, (255, 255, 255))
						elif fast_inventory.selected_item == 2:
							try:
								for bl in fast_inventory.items[fast_inventory.selected_item]:
									bl.rect.left = 89
									bl.rect.top = 25
									item_name = f1.render(bl.name + ': ' + str(len(fast_inventory.items[fast_inventory.selected_item])), 
										True, (255, 255, 255))
							except TypeError:
								item_name = f1.render('пусто', True, (255, 255, 255))
			# управление крафтом
				elif event.key == pg.K_z:
					if show_inventory:
						if show_craft:
							craft.image = craft.image_button
							show_craft = False
						else:
							craft.image = craft.image_craft
							show_craft = True
				elif event.key == pg.K_w:
					if show_craft:
						if selection_craft.rect.top > 20:
							selection_craft.rect.top -= 32
							craft.selected_item -= 1

				elif event.key == pg.K_s:
					if show_craft:
						if selection_craft.rect.top < 212:
							selection_craft.rect.top += 32
							craft.selected_item += 1

				elif event.key == pg.K_RETURN:
					if show_craft:
						if craft.selected_item == 0:
							try:
								if SearchResourses('tree') >= 1:
									for x in range(0, 4):
										AddBlock(cl.Block(
											Textures['BOARDS'],
											[0, 0],
											'board'))
							except TypeError:
								pass
						elif craft.selected_item == 1:
							try:
								if SearchResourses('stone') >= 1:
									AddBlock(cl.Block(
										Textures['BAKE'],
										[0, 0],
										'bake'))
							except TypeError:
								pass
						elif craft.selected_item == 2:
							try:
								if SearchResourses('board') >= 2:
									for x in range(0, 2):
										AddBlock(cl.Block(
											Textures['STAIRS'],
											[0, 0],
											'stairs'))
							except TypeError:
								pass
						elif craft.selected_item == 3:
							try:
								if SearchResourses('board') >= 1:
									for x in range(0, 4):
										AddBlock(cl.Block(
											Textures['PLATFORM'],
											[0, 0],
											'platform'))
							except TypeError:
								pass
						elif craft.selected_item == 4:
							try:
								if SearchResourses('board') >= 2:
									AddBlock(cl.Block(
										Textures['DOOR'],
										[0, 0],
										'door'))
							except TypeError:
								pass
						elif craft.selected_item == 5:
							try:
								if SearchResourses('board') >= 1:
									AddBlock(cl.Block(
										Textures['CASE'],
										[0, 0],
										'case'))
							except TypeError:
								pass
						elif craft.selected_item == 6:
							try:
								if SearchResourses('bamboo') >= 1:
									for x in range(0, 4):
										AddBlock(cl.Block(
											Textures['SUGAR'],
											[0, 0],
											'sugar'))
							except TypeError:
								pass
						SortInventoryItems()
					else:
						for cs in cases:
							if (cs.rect.collidepoint(
								selection.rect.left + 10, 
								selection.rect.top + 10) and cs.open):
								cs.Close
							elif cs.rect.collidepoint(
								selection.rect.left + 10, 
								selection.rect.top + 10):
								cs.Open
	
			elif event.type == pg.KEYUP:
				if event.key == pg.K_d:
					person.moving_right = False
				elif event.key == pg.K_a:
					person.moving_left = False
				elif event.key == pg.K_SPACE:
					person.jump	= False
# обработка столкновений со стенами
	# при ходьбе вправо
		if person.moving_right:
			for bl in blocks:
				if mt.sqrt(abs((person.rect.left + 10) - (bl.rect.left + 10)) ** 2 + 
					abs((person.rect.top + 20) - (bl.rect.top + 10)) ** 2) <= 100:
					if (bl.rect.collidepoint(
						person.rect.left + 20, 
						person.rect.top + 35) or
						bl.rect.collidepoint(
						person.rect.left + 20, 
						person.rect.top + 15)):
						person.moving_right = False
						break
					else:
						person.moving_right = True
			if person.moving_right:
				for br in boards:
					if (br.rect.collidepoint(
						person.rect.left + 20, 
						person.rect.top + 15) or 
						br.rect.collidepoint(
						person.rect.left + 20, 
						person.rect.top + 35)):
						person.moving_right = False
						break
					else:
						person.moving_right = True
				if person.moving_right:
					for br in furniture:
						if (br.rect.collidepoint(
							person.rect.left + 20, 
							person.rect.top + 15) or 
							br.rect.collidepoint(
							person.rect.left + 20, 
							person.rect.top + 35)):
							person.moving_right = False
							break
						else:
							person.moving_right = True
					if person.moving_right:
						for br in platforms:
							if (br.rect.collidepoint(
								person.rect.left + 20, 
								person.rect.top + 15) or 
								br.rect.collidepoint(
								person.rect.left + 20, 
								person.rect.top + 35)):
								person.moving_right = False
								break
							else:
								person.moving_right = True
	
	# при ходьбе влево
		if person.moving_left:
			for bl in blocks:
				if mt.sqrt(abs((person.rect.left + 10) - (bl.rect.left + 10)) ** 2 + 
					abs((person.rect.top + 20) - (bl.rect.top + 10)) ** 2) <= 100:
					if (bl.rect.collidepoint(
						person.rect.left - 1, 
						person.rect.top + 35) or
						bl.rect.collidepoint(
						person.rect.left - 1, 
						person.rect.top + 15)):
						person.moving_left = False
						break
					else:
						person.moving_left = True
			if person.moving_left:
				for br in boards:
					if (br.rect.collidepoint(
						person.rect.left - 1, 
						person.rect.top + 35) or 
						br.rect.collidepoint(
						person.rect.left - 1, 
						person.rect.top + 15)):
						person.moving_left = False
						break
					else:
						person.moving_left = True
				if person.moving_left:
					for br in furniture:
						if (br.rect.collidepoint(
							person.rect.left - 1, 
							person.rect.top + 35) or 
							br.rect.collidepoint(
							person.rect.left - 1, 
							person.rect.top + 15)):
							person.moving_left = False
							break
						else:
							person.moving_left = True
					if person.moving_left:
						for br in platforms:
							if (br.rect.collidepoint(
								person.rect.left - 1, 
								person.rect.top + 35) or 
								br.rect.collidepoint(
								person.rect.left - 1, 
								person.rect.top + 15)):
								person.moving_left = False
								break
							else:
								person.moving_left = True
	
	# обработка прыжков
		if person.jump == False:
			#person_damage += 1
			for bl in blocks:
				if (bl.rect.collidepoint(
					person.rect.left + 15, 
					person.rect.top + 40) or
					bl.rect.collidepoint(
					person.rect.left + 5, 
					person.rect.top + 40)):
					person.fall = False
					break
				else:
					person.fall = True
			if person.fall:
				for br in boards:
					if (br.rect.collidepoint(
						person.rect.left + 15, 
						person.rect.top + 40) or 
						br.rect.collidepoint(
						person.rect.left + 5, 
						person.rect.top + 40)):
						person.fall = False
						break
					else:
						person.fall = True
				if person.fall:
					for br in furniture:
						if (br.rect.collidepoint(
							person.rect.left + 15, 
							person.rect.top + 40) or 
							br.rect.collidepoint(
							person.rect.left + 5, 
							person.rect.top + 40)):
							person.fall = False
							break
						else:
							person.fall = True
					if person.fall:
						for br in platforms:
							if (br.rect.collidepoint(
								person.rect.left + 15, 
								person.rect.top + 40) or 
								br.rect.collidepoint(
								person.rect.left + 5, 
								person.rect.top + 40)):
								person.fall = False
								break
							else:
								person.fall = True

			delta_jump = 0
		else:
			for bl in blocks:
				if (bl.rect.collidepoint(
					person.rect.left + 15, 
					person.rect.top) or
					bl.rect.collidepoint(
					person.rect.left + 5, 
					person.rect.top)):
					person.fall = True 
					person.jump = False
					delta_jump = 0
					break
				else:
					person.fall = False
			if person.jump:
				for br in boards:
					if (br.rect.collidepoint(
						person.rect.left + 15, 
						person.rect.top) or 
						br.rect.collidepoint(
						person.rect.left + 5, 
						person.rect.top)):
						person.fall = True
						person.jump = False
						delta_jump = 0
						break
					else:
						person.fall = False
				if person.jump:
					for br in furniture:
						if (br.rect.collidepoint(
							person.rect.left + 15, 
							person.rect.top) or 
							br.rect.collidepoint(
							person.rect.left + 5, 
							person.rect.top)):
							person.fall = True
							person.jump = False
							delta_jump = 0
							break
						else:
							person.fall = False
			if delta_jump <= 10:
				delta_jump += 1
			else:
				person.jump = False
	
	# проверка выбора блока на выход за границы экрана
		if selection.rect.left >= 800:
			selection.rect.left = 0
		elif selection.rect.left < 0:
			selection.rect.left = 780
		if selection.rect.top >= 600:
			selection.rect.top = 0
		elif selection.rect.top < 0:
			selection.rect.top = 580
		if (person.rect.left + 10) - (selection.rect.left + 10) > 80:
			selection.rect.left += 20 
		elif (person.rect.left + 10) - (selection.rect.left + 10) < -80:
			selection.rect.left -= 20 
		if (person.rect.top + 20) - (selection.rect.top + 10) > 80:
			selection.rect.top += 20 
		elif (person.rect.top + 20) - (selection.rect.top + 10) < -80:
			selection.rect.top -= 20 
	
		person.UPDATE()
	
		if person.helth > 20:
			person_helth = f1.render('НР: ' + str(person.helth), True, (255, 255, 255))
		else:
			person_helth = f1.render('НР: ' + str(person.helth), True, (255, 0, 0))
# отрисовка объектов
		sc.blit(background.image, background.rect)
		for lv in leaves:
			sc.blit(lv.image, lv.rect)
		for tr in trees:
			sc.blit(tr.image, tr.rect)
		for cs in cases:
			sc.blit(cs.image, cs.rect)
		sc.blit(person.image, person.rect)
		sc.blit(fast_inventory.image, fast_inventory.rect)
		sc.blit(selection_item.image, selection_item.rect)
		for bl in blocks:
			sc.blit(bl.image, bl.rect)
		for br in boards:
			sc.blit(br.image, br.rect)
		for fr in furniture:
			sc.blit(fr.image, fr.rect)
		for pl in platforms:
			sc.blit(pl.image, pl.rect)
		try:
			sc.blit(item_name, (20, 56))
		except TypeError:
			item_name = f1.render('пусто', True, (255, 255, 255))
		sc.blit(person_helth, (730, 30))
		sc.blit(game_exit.image, game_exit.rect)
		if show_inventory:
			sc.blit(craft.image, craft.rect)
			if show_craft:
				sc.blit(selection_craft.image, selection_craft.rect)
			sc.blit(inventory.image, inventory.rect)
			for it in inventory.items:
				try:
					for bl in it:
						sc.blit(bl.image, bl.rect)
						break
				except TypeError:
					pass
			sc.blit(selection_inventory.image, selection_inventory.rect)
			sc.blit(inventory_item_name, (220, 160))
		else:
			sc.blit(selection.image, selection.rect)
		for it in fast_inventory.items:
			try:
				for bl in it:
					sc.blit(bl.image, bl.rect)
					break
			except TypeError:
				pass
	
		pg.display.update()
		clock.tick(FPS)
