import pygame
import sys

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer Game")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

GRAVITY = 0.8

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)

# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

# ---------------- PLATFORM ----------------
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left, right):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.left = left
        self.right = right
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= self.left or self.rect.right >= self.right:
            self.speed *= -1

# ---------------- LEVEL DATA ----------------
levels = [
    {
        "platforms": [(0, 460, 800, 40), (200, 350, 120, 20), (400, 280, 120, 20)],
        "coins": [(230, 320), (430, 250)],
        "enemies": [(300, 420, 300, 500)]
    },
    {
        "platforms": [(0, 460, 800, 40), (150, 360, 120, 20), (350, 300, 120, 20), (550, 240, 120, 20)],
        "coins": [(180, 330), (380, 270), (580, 210)],
        "enemies": [(200, 420, 200, 400), (500, 420, 500, 700)]
    }
]

# ---------------- LOAD LEVEL ----------------
def load_level(index):
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    for p in levels[index]["platforms"]:
        platforms.add(Platform(*p))

    for c in levels[index]["coins"]:
        coins.add(Coin(*c))

    for e in levels[index]["enemies"]:
        enemies.add(Enemy(*e))

    return platforms, coins, enemies

# ---------------- GAME SETUP ----------------
level_index = 0
player = Player(50, 400)
platforms, coins, enemies = load_level(level_index)

score = 0

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(platforms)
    enemies.update()

    # Coin collision
    collected = pygame.sprite.spritecollide(player, coins, True)
    score += len(collected)

    # Enemy collision
    if pygame.sprite.spritecollide(player, enemies, False):
        player.rect.topleft = (50, 400)
        score = 0

    # Level complete
    if len(coins) == 0:
        level_index += 1
        if level_index >= len(levels):
            text = FONT.render("YOU WIN!", True, BLUE)
            screen.blit(text, (WIDTH//2 - 70, HEIGHT//2))
            pygame.display.update()
            pygame.time.wait(3000)
            break
        platforms, coins, enemies = load_level(level_index)
        player.rect.topleft = (50, 400)

    # Draw
    platforms.draw(screen)
    coins.draw(screen)
    enemies.draw(screen)
    screen.blit(player.image, player.rect)

    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    level_text = FONT.render(f"Level: {level_index + 1}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.update()

pygame.quit()
sys.exit()
