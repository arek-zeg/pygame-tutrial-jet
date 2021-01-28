import pygame
import random
from pygame import sprite
from pygame.constants import K_LEFT
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


class Player(pygame.sprite.Sprite):

    def __init__(self, score=0):
        super().__init__()
        self.surf = pygame.image.load(
            'd:/vsc-python/game1/jet.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(0, windowHeight/2))
        self.score = score

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # keep on screen
        if self.rect.top <= 30:
            self.rect.top = 30
        if self.rect.bottom >= windowHeight:
            self.rect.bottom = windowHeight
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > windowWidth:
            self.rect.right = windowWidth

    def get_score(self):
        if self.score <= 1000:
            return str(self.score) + ' m'
        if self.score > 1000:
            return str(self.score)[:-3] + ' km'

    def show_score(self, screen):
        screen.fill((0, 0, 0))
        self.myfont = pygame.font.SysFont('Calibri', 50)
        self.label = self.myfont.render(self.get_score(), 1, (0, 255, 0))
        screen.blit(self.label, (screen.get_width()/2 - 50, (screen.get_height()/2 - 40)))


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(random.randint(windowWidth + 20, windowWidth + 100),
                                               random.randint(30, windowHeight))
                                       )
        self.speed = random.randint(5, 20)

    def update(self, player):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(
            'd:/vsc-python/game1/cloud.png').convert()
        self.surf.set_colorkey((17, 193, 242), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(windowWidth + 20, windowWidth + 100),
                                               random.randint(50, windowHeight))
                                       )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class DistanceCounter:
    def __init__(self):
        self.myfont = pygame.font.SysFont('Calibri', 20)

    def update(self, player, screen):
        self.label = self.myfont.render(
            'Distance ' + player.get_score(), True, 'yellow')
        screen.blit(self.label, (5, 5))


pygame.init()

windowWidth = 800
windowHeight = 600

screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()
addEnemy = pygame.USEREVENT + 1
pygame.time.set_timer(addEnemy, 250)
addCloud = pygame.USEREVENT + 2
pygame.time.set_timer(addCloud, 750)

player1 = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
playerScore = DistanceCounter()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)


running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == addEnemy:
            newEnemy = Enemy()
            enemies.add(newEnemy)
            all_sprites.add(newEnemy)
        elif event.type == addCloud:
            newCloud = Cloud()
            clouds.add(newCloud)
            all_sprites.add(newCloud)

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    enemies.update(player1)
    clouds.update()

    screen.fill((17, 193, 242))

    playerScore.update(player1, screen)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player1, enemies):
        player1.kill()
        running = False

    pygame.display.flip()
    player1.score += 1
    clock.tick(30)


running1 = True
while running1:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running1 = False
        elif event.type == QUIT:
            running1 = False

    screen.fill((17, 193, 242))

    player1.show_score(screen)

    pygame.display.flip()


pygame.quit()
