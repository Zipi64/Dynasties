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

background = (144, 201, 200)
# Риосвание заднего фона
def draw_background():
	screen.fill(background)
# Класс игрока
class Player(pygame.sprite.Sprite):
	def __init__(self, type, x, y, speed, scale):
		pygame.sprite.Sprite.__init__(self)
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




# Создание игрока
# mob = Player('Mob', 250, 250, 5, 1.5) # доделать картинки с мобом
player = Player('Player', 250, 250, 5, 1.5)
# Игровой цикл
running = True
while(running):
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
	pygame.display.update()
pygame.quit()