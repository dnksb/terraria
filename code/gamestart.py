import pygame 
from game_lvl import Game
import classes as cl

pygame.init()
clock = pygame.time.Clock()
fps = 60
size = (800, 600)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Kazakhstan")

game_exit = cl.Texture(F'exit.png', [40, 480])
start_game = cl.Texture(F'start_game.png', [40, 410])
start_game_cheat = cl.Texture(F'start_game_cheat.png', [205, 420])

# создание заднего фона
background = cl.Texture(
	F'background_menu.jpg',
	[0, 0])

def GameMenu():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos  
				if game_exit.rect.collidepoint(mouse_pos):
					return
				elif start_game.rect.collidepoint(mouse_pos):
					Game(False)
				elif start_game_cheat.rect.collidepoint(mouse_pos):
					Game(True)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					Game(False)
				elif event.key == pygame.K_ESCAPE:
					return
		screen.blit(background.image, background.rect)
		screen.blit(game_exit.image, game_exit.rect)
		screen.blit(start_game.image, start_game.rect)
		screen.blit(start_game_cheat.image, start_game_cheat.rect)
		pygame.display.update()
		clock.tick(fps)
GameMenu()	
pygame.quit()
