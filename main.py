import pygame
import os
pygame.init()
screen = pygame.display.set_mode((800, 640)) # Размеры окна
pygame.display.set_caption("Dynasties")

# Часы
clock = pygame.time.Clock()
FPS = 60

# Состояние перемещения игрока
move_right = False
move_left = False

background = (144, 201, 200)
# Риосвание заднего фона
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
	def __init__(self, type, x, y, speed, scale):
		pygame.sprite.Sprite.__init__(self)
		self.animation = "stay"
		self.cut_sheet(load_image("Player/Idle/Idle-Sheet.png"), 4, 1)
		self.type = type
		self.speed = speed
		self.direction = 1
		self.rotation = False
		character_img = pygame.image.load(f'data/{type}/Idle/Idle.gif')
		self.image = pygame.transform.scale(character_img, (int(character_img.get_width() * scale), (int(character_img.get_height() * scale))))
		self.rect = self.image.get_rect()
		self.rect.center = (x , y)
	
		
	# Рисование персонажа и его поворот
	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.rotation, False), self.rect)
    
	# Движение персонжа
	def move(self, move_left, move_right):
		# Изменение положение персонажа
		dx = 0
		dy = 0
		if move_right:
			dx = self.speed
			self.rotation = False
			self.direction = 1
		if move_left:
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
		print(self.cur_frame)
		




# Создание игрока
# mob = Player('Mob', 250, 250, 5, 1.5) # доделать картинки с мобом
player = Player('Player', 250, 250, 5, 1.5)
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
		
		# Кнопка отпущена
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a: # Перемещение влево
				move_left = False
			if event.key == pygame.K_d:
				move_right = False #  Перемещение вправо
			if event.key == pygame.K_ESCAPE: # Закрытие игры по клавише ESC
				running = False 
		
		if move_left or move_right:
			if not player.animation == "moving":
				player.cut_sheet(load_image("Player/Run/Run-Sheet.png"), 8, 1)
				player.animation = "moving"
		else:
			if not player.animation == "stay":
				player.cut_sheet(load_image("Player/Idle/Idle-Sheet.png"), 4, 1)
				player.animation = "stay"

	player.update()
	pygame.display.update()
pygame.quit()