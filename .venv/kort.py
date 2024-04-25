import pygame
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


WIDTH = 800
HEIGHT = 600


PLAYER_SIZE = 50
PLAYER_SPEED = 5


ENEMY_SIZE = 30
ENEMY_SPEED = 2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -ENEMY_SIZE)
        self.speedy = random.randrange(ENEMY_SPEED // 2, ENEMY_SPEED)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -ENEMY_SIZE)
            self.speedy = random.randrange(ENEMY_SPEED // 2, ENEMY_SPEED)


class StrongEnemy(Enemy):
    def __init__(self):
        super().__init__(RED, ENEMY_SIZE + 10, ENEMY_SIZE + 10)
        self.speedy = random.randrange(ENEMY_SPEED - 1, ENEMY_SPEED + 3)

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__(BLUE, ENEMY_SIZE + 12, ENEMY_SIZE + 12)
        self.speedy = random.randrange(ENEMY_SPEED - 1, ENEMY_SPEED + 4)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Skapa en klass för skotten (bullets)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 5])  # Storlek på skott
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arv och Pygame")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Lägg till fiender till spritegruppen
for _ in range(8):
    enemy = Enemy(BLACK, ENEMY_SIZE, ENEMY_SIZE)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Spellopp
running = True
while running:

    clock.tick(60)

    # Hantera händelser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Uppdatera
    all_sprites.update()

    # Kollisioner - fiender och skott
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:

        enemy = Enemy(BLACK, ENEMY_SIZE, ENEMY_SIZE)

        enemies.add(enemy)
        enemy = StrongEnemy()
        all_sprites.add(enemy)
        enemies.add(enemy)


    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:

        enemy = Enemy(BLACK, ENEMY_SIZE, ENEMY_SIZE)
        all_sprites.add(enemy)
        enemies.add(enemy)
        enemy = StrongEnemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    screen.fill(WHITE)


    all_sprites.draw(screen)


    pygame.display.flip()

pygame.quit()
