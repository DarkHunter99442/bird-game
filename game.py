"""
Dodge Game (Python + Pygame)

Run:
1) Install pygame if needed: pip install pygame
2) Save this file as dodge_game.py and run: python dodge_game.py

Controls:
- Left / Right arrow keys or A / D to move
- Space to pause/unpause
- Esc to quit

Simple single-file game with Bengali comments so you can understand ও কাস্টমাইজ করতে পারো।
"""

import pygame
import random
import sys
import os

# --------------------
# শুরু কনফিগ
# --------------------
WIDTH, HEIGHT = 720, 480
FPS = 60
PLAYER_SPEED = 6
OBSTACLE_MIN = 18
OBSTACLE_MAX = 60
SPAWN_INTERVAL = 800  # মিলিসেকেন্ড
HIGH_FILE = 'dodge_high.txt'

# --------------------
# হাইস্কোর লোড/সেভ
# --------------------
def load_high():
    try:
        with open(HIGH_FILE, 'r') as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0

def save_high(h):
    try:
        with open(HIGH_FILE, 'w') as f:
            f.write(str(int(h)))
    except Exception:
        pass

# --------------------
# গেম ইনিশিয়ালাইজ
# --------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodge Game - Python')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

highscore = load_high()

# প্লেয়ার অবজেক্ট
player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 70, 40, 40)
player_color = (56, 189, 248)

obstacles = []  # list of dicts: {'rect': pygame.Rect, 'speed': float}

score = 0
lives = 3
running = True
paused = False
last_spawn = pygame.time.get_ticks()

# --------------------
# হেল্পার ফাংশন
# --------------------

def spawn_obstacle():
    w = random.randint(OBSTACLE_MIN, OBSTACLE_MAX)
    x = random.randint(10, WIDTH - w - 10)
    r = pygame.Rect(x, -w, w, w)
    speed = random.uniform(2.0, 4.0) + score * 0.02
    obstacles.append({'rect': r, 'speed': speed})


def draw_text(s, x, y, color=(230, 238, 246)):
    img = font.render(s, True, color)
    screen.blit(img, (x, y))

# --------------------
# মেইন লুপ
# --------------------
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused

    keys = pygame.key.get_pressed()
    if not paused:
        vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = PLAYER_SPEED
        player.x += vx
        # সীমা
        if player.x < 8:
            player.x = 8
        if player.x + player.width > WIDTH - 8:
            player.x = WIDTH - 8 - player.width

        # স্পন
        now = pygame.time.get_ticks()
        if now - last_spawn > max(200, SPAWN_INTERVAL - score*6):
            spawn_obstacle()
            last_spawn = now

        # বাধা আপডেট
        for ob in obstacles[:]:
            ob['rect'].y += ob['speed']
            if ob['rect'].top > HEIGHT:
                obstacles.remove(ob)
                score += 1
            elif ob['rect'].colliderect(player):
                obstacles.remove(ob)
                lives -= 1
                if lives <= 0:
                    # গেম ওভার
                    if score > highscore:
                        highscore = score
                        save_high(highscore)
                    # এক -- alert রকম
                    print(f"Game Over — Score: {score}, Highscore: {highscore}")
                    # রিসেট
                    score = 0
                    lives = 3
                    obstacles.clear()

    # রেন্ডার
    screen.fill((7, 16, 36))  # ব্যাকগ্রাউন্ড

    # গ্রিড/লাইন না হলে সুন্দর দেখাবে
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (10, 22, 44), (0, i), (WIDTH, i), 1)

    # প্লেয়ার
    pygame.draw.rect(screen, player_color, player, border_radius=6)
    # প্লেয়ার ছায়া
    shadow = pygame.Rect(player.x + 6, player.y + player.height + 8, player.width - 12, 6)
    pygame.draw.rect(screen, (3,7,18), shadow)

    # বাধা ড্র
    for ob in obstacles:
        pygame.draw.rect(screen, (251,113,133), ob['rect'], border_radius=6)

    # HUD
    draw_text(f"Score: {score}", 12, 12)
    draw_text(f"Lives: {lives}", 140, 12)
    draw_text(f"High: {highscore}", 240, 12)
    if paused:
        draw_text("PAUSED - Press Space to resume", WIDTH//2 - 140, HEIGHT//2 - 12, (180,180,180))

    pygame.display.flip()

pygame.quit()
sys.exit()

v=00000000000000