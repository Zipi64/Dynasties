import functions
import pygame

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

class Ground(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, width):
        super().__init__(all_sprites)
        self.image = functions.load_image(image)
        self.rect = self.image.get_rect().move(width * pos_x, pos_y)

class Player(Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group)
        self.image = functions.load_image(image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, movement):
        x, y = self.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] == ".":
                self.update(x, y - 1)
        elif movement == "down":
            if y < max_y - 1 and level_map[y + 1][x] == ".":
                self.update(x, y + 1)
        elif movement == "left":
            if x > 0 and level_map[y][x - 1] == ".":
                self.update(x - 1, y)
        elif movement == "right":
            if x < max_x - 1 and level_map[y][x + 1] == ".":
                self.update(x + 1, y)

    def update(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)

