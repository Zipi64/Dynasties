import os
import sys

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 640)) # Размеры окна
pygame.display.set_caption("Dynasties")

# Часы
clock = pygame.time.Clock()
FPS = 60

# Состояние перемещения игрока
move_right = False
move_left = False
move_up = False

# Риосвание заднего фона
background = (144, 201, 200)

# Загрузка музыки
pygame.mixer.music.load('data/audio/main.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

STAY = "Player/Idle/Idle-Sheet.png"
MOVE = "Player/Run/Run-Sheet.png"
JUMP = "Player/Jump-All/Jump-All-Sheet.png"
def draw_background():
	screen.fill(background)

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

# Класс игрока
class Player(pygame.sprite.Sprite):
	def __init__(self, type, x, y, speed):
		pygame.sprite.Sprite.__init__(self)
		self.animation = "stay"
		self.x = x
		self.y = y
		self.stay_animation()
		self.type = type
		self.speed = speed
		self.direction = 1
		self.rotation = False
		self.jumping = False
		self.rect = self.image.get_rect()
		self.rect.center = (x , y)
	
		
	# Рисование персонажа и его поворот
	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.rotation, False), self.rect)
	
	def stay_animation(self):
		self.cut_sheet(load_image(STAY), 4, 1)
    
	# Движение персонжа
	def move(self, move_left, move_right):
		# Изменение положение персонажа
		dx = 0
		dy = 0
		if move_right:
			dx = self.speed
			self.rotation = False
			self.direction = 1
		if move_left and self.x > 5:
			dx = -self.speed
			self.rotation = True
			self.direction = -1
		# Движение персонажа
		self.rect.x += dx
		self.rect.y += dy
	
	# Вырезание анимации 
	def cut_sheet(self, sheet, columns, rows):
		self.counter = 0
		self.frames = []
		self.temprect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
		for j in range(rows):
			for i in range(columns):
				frame_location = (self.temprect.w * i, self.temprect.h * j)
				self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.temprect.size)))
		self.cur_frame = 0
		self.image = self.frames[self.cur_frame]

	# Изменение анимации
	def update(self):
		if self.counter != 8:
			self.counter += 1
			return
		self.counter = 0
		self.cur_frame = (self.cur_frame + 1) % len(self.frames)
		self.image = self.frames[self.cur_frame]
		if self.jumping and self.cur_frame == 14:
			self.jumping = False
			self.animation = "stay"
			self.stay_animation()
			return
		




# Создание игрока
player = Player('Player', 50, 600, 5)
# Игровой цикл
running = True
while running:
	draw_background()
	clock.tick(FPS) # Установка FPS
	player.draw() # Рисование персонажа
	#mob.draw()
	player.move(move_left, move_right) # Передвижение персонажа
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # Закрытие окна
			running = False
		# Кнопка нажата
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a: # Перемещение влево
				move_left = True
			if event.key == pygame.K_d:
				move_right = True #  Перемещение вправо
			if event.key == pygame.K_SPACE:
				move_up = True
				player.jumping = True
		
		# Кнопка отпущена
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a: # Перемещение влево
				move_left = False
			if event.key == pygame.K_d:
				move_right = False #  Перемещение вправо
			if event.key == pygame.K_SPACE:
				move_up = False
			if event.key == pygame.K_ESCAPE: # Закрытие игры по клавише ESC
				running = False 
		if move_up or player.jumping:
			if not player.animation == "jump":
				player.cut_sheet(load_image(JUMP), 15, 1)
				player.animation = "jump"

		elif move_left or move_right:
			if not player.animation == "moving":
				player.cut_sheet(load_image(MOVE), 8, 1)
				player.animation = "moving"
		else:
			if not player.animation == "stay":
				player.cut_sheet(load_image(STAY), 4, 1)
				player.animation = "stay"
	player.update()
	pygame.display.update()
pygame.quit()