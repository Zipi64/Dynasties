import os
import sys
import pygame
from pygame import *

pygame.font.init()
pygame.init()
size =  width, height = 950, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Dynasties")

# Полноэкранный режим
current_size = screen.get_size() # Текущее разрешение
display_info = pygame.display.Info() # Максимальное разрешение
fullscreen_size = (display_info.current_w, display_info.current_h) # Кортеж разрешения экрана
is_fullscreen = False # Проверка на полноэкранный режим
last_size = current_size

# Часы
clock = pygame.time.Clock()
FPS = 60

# Состояние перемещения игрока
move_right = False
move_left = False
move_up = False
hit = False
coins = 0 # Количество собранных монет

GAMEOVER = False

# Риосвание заднего фона
background_image = pygame.image.load('data/background/background.png')

# Расположение анимаций
STAY = "Player/Idle/Idle-Sheet.png"
MOVE = "Player/Run/Run-Sheet.png"
JUMP = "Player/Jump-All/Jump-All-Sheet.png"
ATTACK = "Player/Attack-01/Attack-01-Sheet.png"
DEATH = "Player/Dead/Dead-Sheet.png"

def show_menu():
	pygame.mixer.music.load('data/audio/menu.wav')
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1, 0.0, 5000)
	menu_background = pygame.image.load('data/menu/menu.png')
	button_new_game = Button(300, 70)
	button_credits = Button(300, 70)
	button_exit = Button(300, 70)
	button_close_credits = Button(300, 70)
	menu = True
	credits_menu = False
	def func_new_game():
		nonlocal menu
		menu = False

	def func_close_credits():
		nonlocal credits_menu
		credits_menu = False

	def func_open_credits():
		nonlocal credits_menu
		credits_menu = True

	while menu:
		screen.blit(menu_background, (0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		button_new_game.draw(325, 120, 'New game', func_new_game, 60)
		button_credits.draw(325, 250, 'Credits', func_open_credits, 60)
		while credits_menu:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			screen.blit(menu_background, (0, 0))
			button_close_credits.draw(50, 500, "Close", func_close_credits, 60)
			print_text('zzzpize.t.me', 385, 225)
			print_text('Queeenace', 385, 275)
			pygame.display.update()
			clock.tick(60)
		button_exit.draw(325, 380, 'Exit', sys.exit , 60)
		pygame.display.update()
		clock.tick(60)


def default_values():  # Дефолтные значения(обновляются после смерти)
	global GAMEOVER, move_right, move_left, move_up, hit, coins, player
	GAMEOVER = False
	move_right = False
	move_left = False
	move_up = False
	hit = False
	coins = 0 # Количество собранных монет
	player = Player('Player', 20, 525, 5)

# Рисование заднего фона
def draw_background():
	screen.blit(background_image, (0, 0))

# Печать текста на экран
def print_text(message, x, y, font_color=(0, 0, 0), font_type='pingpong.ttf', font_size=30):
	font_type = pygame.font.Font(font_type, font_size)
	text = font_type.render(message, True, font_color)
	screen.blit(text, (x, y))

# Игра закончена
def game_over():
	pygame.mixer.music.stop() # Прекращение музыки после смерти :(
	global GAMEOVER
	GAMEOVER = True
	while GAMEOVER:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # Закрытие окна
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_r:  # Перезапуск игры
					default_values()
		print_text('YOU DIED! Press R to restart or ESC to exit.', 175, 250)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			GAMEOVER = False
		display.update()
		clock.tick(60)

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


# Класс кнопки
class Button:
	def __init__(self, width, height) -> None:
		self.width = width
		self.height = height
		self.inactive_color = (13, 162, 58)
		self.active_color = (23, 204, 58)
	
	def draw(self, x, y, message, action=None, font_size=30):
		mouse = pygame.mouse.get_pos()
		is_click = pygame.mouse.get_pressed()

		# Подсвечивание кнопки
		if x < mouse[0] < x + self.width:
			if y < mouse[1] < y + self.height:
				pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

				if is_click[0] == 1:
					if action is not None:
						action()
		else:
			pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
		
		print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


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
		if not self.alive:
			return
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
				dy = -2
			else:
				dy = 2
		self.rect.x += dx
		self.rect.y += dy
		x = self.rect.x
		y = self.rect.y
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
			self.rect.y -= 2
			self.stay_animation()
			return
		if self.jumping:
			self.jump_count += 1



# Создание игрока
show_menu()
player = Player('Player', 20, 525, 5)
pygame.mixer.music.load('data/audio/main.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
# -------- Основной игровой цикл -----------
running = True
while running:
	# Кнопка рандомная для теста
	clock.tick(FPS) # Установка FPS
	draw_background()
	player.draw() # Рисование персонажа
	player.move(move_left, move_right)  # Передвижение персонажа
	for event in pygame.event.get():
		if event.type == pygame.QUIT:  # Закрытие окна
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F11: # Полноэкранный режим на F11
				is_fullscreen = not is_fullscreen
				if is_fullscreen:
					last_size = current_size
					current_size = fullscreen_size
					screen = pygame.display.set_mode(current_size, FULLSCREEN)
				else:
					current_size = last_size
					screen = pygame.display.set_mode(current_size, RESIZABLE)
					screen = pygame.display.set_mode(current_size, RESIZABLE) # Решение бага с полноэкранным режимом

		# Кнопка нажата
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:  # Перемещение влево
				move_left = True
			if event.key == pygame.K_d:  # Перемещение вправо
				move_right = True
			if event.key == pygame.K_SPACE and not hit and not player.hitting:
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
		
		if (
			event.type == pygame.MOUSEBUTTONDOWN # Кнопка нажата
			and event.button == 1
			and not move_up
			and not player.jumping
		):
			hit = True
			player.hitting = True

		if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Кнопка отпущена 
			hit = False

		if not player.alive:
			if not player.animation == "death":
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
		if player.cur_frame == 7 and not player.alive:
			player.last_animation = True
			game_over()
		player.update()
		pygame.display.update()
pygame.quit()