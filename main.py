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
hit = False

# Риосвание заднего фона
background = (144, 201, 200)

# Загрузка музыки
pygame.mixer.music.load('data/audio/main.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# Расположение анимаций
STAY = "Player/Idle/Idle-Sheet.png"
MOVE = "Player/Run/Run-Sheet.png"
JUMP = "Player/Jump-All/Jump-All-Sheet.png"
ATTACK = "Player/Attack-01/Attack-01-Sheet.png"
DEATH = "Player/Dead/Dead-Sheet.png"

# Рисование заднего фона
def draw_background():
	screen.fill(background)

# Загрузка изображений
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
		self.jump_count = 0
		self.hitting = False
		self.attack_range = {
			"x1": x,
			"x2": x + 50,
			"y1": y - 25,
			"y2": y + 25
		}
		self.hitbocks = {
			"top": (x - 10, y - 25),
			"bottom": (x + 10, y + 25) 
		}
		self.rect = self.image.get_rect()
		self.rect.center = (x , y)
		self.alive = True
		self.last_animation = False

	
		
	# Рисование персонажа и его поворот
	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.rotation, False), self.rect)
	
	# Анимация стояния
	def stay_animation(self):
		self.animation = "stay"
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
		if self.jumping:
			if self.jump_count <= 6:
				dy = -1
			else:
				dy = 1
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
		timings = 3 if self.jumping else 5 if self.hitting else 8  # Определение, раз в сколько кадров анимация
		if self.counter != timings:
			self.counter += 1
			return
		self.counter = 0
		self.cur_frame = (self.cur_frame + 1) % len(self.frames)
		self.image = self.frames[self.cur_frame]


		if self.hitting and self.cur_frame == 7:  # Если атака
			self.hitting = False
			self.stay_animation()

		if self.jumping and self.cur_frame == 14:  # Если прыжок
			self.jumping = False
			self.jump_count = 0
			self.rect.y -= 1
			self.stay_animation()
			return
		if self.jumping:
			self.jump_count += 1
		
# Создание игрока
player = Player('Player', 50, 600, 5)
# Игровой цикл
running = True

while running:
	draw_background()
	clock.tick(FPS) # Установка FPS
	player.draw() # Рисование персонажа
	#mob.draw()
	player.move(move_left, move_right)  # Передвижение персонажа
	for event in pygame.event.get():
		if event.type == pygame.QUIT:  # Закрытие окна
			running = False
		# Кнопка нажата
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:  # Перемещение влево
				move_left = True
			if event.key == pygame.K_d:  # Перемещение вправо
				move_right = True 
			if event.key == pygame.K_SPACE:
				if not (hit or player.hitting):
					move_up = True
					player.jumping = True
					
			if event.key == pygame.K_p:  # Кнопка для смерти
				player.alive = False
				player.rect.y += 15
		
		# Кнопка отпущена
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:  # Перемещение влево
				move_left = False
			if event.key == pygame.K_d:  # Перемещение вправо
				move_right = False  
			if event.key == pygame.K_SPACE:  # Прыжок
				move_up = False
			if event.key == pygame.K_ESCAPE:  # Закрытие игры по клавише ESC
				running = False 
		
		if event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие на кнопку мыши
			if event.button == 1 and not (move_up or player.jumping):
				hit = True
				player.hitting = True
		
		if event.type == pygame.MOUSEBUTTONUP:  # Отпускание кнопки мыши
			if event.button == 1:
				hit = False

		if not player.alive:
			player.cut_sheet(load_image(DEATH), 8, 1)
			player.animation = "death"

		elif (move_up or player.jumping):
			if not player.animation == "jump":
				player.cut_sheet(load_image(JUMP), 15, 1)
				player.animation = "jump"

		elif hit or player.hitting:
			if not player.animation == "attack":
				player.cut_sheet(load_image(ATTACK), 8, 1)
				player.animation = "attack"

		elif move_left or move_right:
			if not player.animation == "moving":
				player.cut_sheet(load_image(MOVE), 8, 1)
				player.animation = "moving"
		else:
			if not player.animation == "stay":
				player.cut_sheet(load_image(STAY), 4, 1)
				player.animation = "stay"
			
	if (not player.alive and player.cur_frame <= 7 and not player.last_animation) or player.alive: # Огромная проверка на то, жив чел или нет
		if player.cur_frame == 7:
			player.last_animation = True
		player.update()
		pygame.display.update()
pygame.quit()