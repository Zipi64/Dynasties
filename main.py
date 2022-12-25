import pygame
import sprites


pygame.init()
screen = pygame.display.set_mode((500, 500)) # Размеры окна
pygame.display.set_caption("Dynasties")

running = True
while(running):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

pygame.quit()