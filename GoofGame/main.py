import pygame as py
import math, time, os, random
from pathlib import Path
py.init()

cwd = Path.cwd()
pygame_dir = cwd / "GoofGame"
assets_dir = pygame_dir / "Assets"
stuff_dir = assets_dir / "Stuff"
dmg_dir = stuff_dir / "dmg"
atk_dir = stuff_dir / "Atks"
hp_dir = stuff_dir / "hp"
audio_dir = assets_dir / "Audio"

py.display.set_caption('Dodge And Come')
py.display.set_icon(py.image.load(assets_dir / "slime-icon-2.jpg"))

bg_p = assets_dir / "pixel-art-grass.png"
bg = py.image.load(bg_p)
bg = py.transform.scale(bg, (bg.get_width() // 2.1, bg.get_height() // 2.1))

bg_music = py.mixer.Sound(audio_dir / "1-19. Through the Woods (Forest Area).mp3")
ding = py.mixer.Sound(audio_dir / "Ding.mp3")
squish = py.mixer.Sound(audio_dir / "Squish.mp3")

bg_music.set_volume(0.1)
ding.set_volume(0.3)
squish.set_volume(0.3)

win_1 = py.mixer.Sound(audio_dir / "1Win.mp3")
win_2 = py.mixer.Sound(audio_dir / "2Win.mp3")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 900, 600
WIN = py.display.set_mode((WIDTH, HEIGHT))

BULLET_SPEED = 5
BULLET_RADIUS = 5

PLAYER1_HIT = py.USEREVENT + 1
PLAYER2_HIT = py.USEREVENT + 2

bbg_p = assets_dir / "blue bg.png"
bbg = py.image.load(bbg_p)
bbg = py.transform.scale(bbg, (bbg.get_width() // 2.1, bbg.get_height() // 2.1))

m_music = py.mixer.Sound(audio_dir / "03 Labyrinth Entrance Stage.mp3")
m_music.set_volume(0.2)

def display():
    WIN.blit(bbg,(0,0))
    button_img = py.image.load(assets_dir / "Enter.png")
    button_img = py.transform.scale(button_img, (button_img.get_width() * 12, button_img.get_height() * 12))

    title_img = py.image.load(assets_dir / "TITLE.png")
    title_img = py.transform.scale(title_img, (title_img.get_width() * 1.2, title_img.get_height() * 1.2))

    press_img = py.image.load(assets_dir / "Press.png")
    press_img = py.transform.scale(press_img, (press_img.get_width() // 2, press_img.get_height() // 2))

    play_img = py.image.load(assets_dir / "ToPlay.png")
    play_img = py.transform.scale(play_img, (play_img.get_width() // 2.5, play_img.get_height() // 2.5))

    WIN.blit(title_img,(75,25))
    WIN.blit(press_img,(550,80))
    WIN.blit(play_img,(170, 400))
    WIN.blit(button_img,(WIDTH // 2 + 150 ,HEIGHT // 2))

    py.display.update()

def menu():
    m_music.play()
    os.system('cls')
    CLOCK = py.time.Clock()
    while True:
        CLOCK.tick(60)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    m_music.stop()
                    main()
            
        display()

class Player:
    def __init__(self, x, y, speed, hp, type, score):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed / 10
        sprite_p = assets_dir / type
        sprite = py.image.load(sprite_p)
        sprite = py.transform.scale(
            sprite, (sprite.get_width() * 1.8, sprite.get_height() * 1.8))
        self.type = sprite
        self.score = score

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

WINNER_FONT = py.font.SysFont("freesansbold", 100)
SCORE_FONT = py.font.SysFont("freesansbold", 70)

def draw_winner(text, win):
    if win:
        win_1.play()
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
        py.display.update()
        py.time.delay(3000)
    else:
        win_2.play()
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
        py.display.update()
        py.time.delay(3000)

def main():
    bg_music.play()
    os.system('cls')
    CLOCK = py.time.Clock()
    blockSize = 60

    player1 = Player(7, 5, 5, 15, "C1.png", 0)
    player2 = Player(9, 7, 5, 15, "C2.png", 0)
    players = [player1, player2]
    bullets = []

    bullet_hit_events = {
        player1: PLAYER1_HIT,
        player2: PLAYER2_HIT
    }

    win = None
    winner_text = ""

    spawn_rate = 0.01
    bullet_type = False

    switch_time = time.time() + random.uniform(1, 10)
    start_time = time.time()
    while True:
        CLOCK.tick(60)
        for event in py.event.get():
            if bullet_type == True:
                if event.type == PLAYER1_HIT:
                    player1.hp -= 1
                    squish.play()
                if event.type == PLAYER2_HIT:
                    player2.hp -= 1
                    squish.play()

            if bullet_type == False:
                if event.type == PLAYER1_HIT:
                    player1.score += 1
                    ding.play()
                if event.type == PLAYER2_HIT:
                    player2.score += 1
                    ding.play()

            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYDOWN:
                # First Player
                if event.key == py.K_w and player1.y - player1.speed >= 1:
                    player1.move(0, -player1.speed)
                elif event.key == py.K_a and player1.x - player1.speed >= 1:
                    player1.move(-player1.speed, 0)
                elif event.key == py.K_s and player1.y - player1.speed <= 9:
                    player1.move(0, player1.speed)
                elif event.key == py.K_d and player1.x + player1.speed <= 15:
                    player1.move(player1.speed, 0)
                # Second Player
                if event.key == py.K_UP and player2.y - player2.speed >= 1:
                    player2.move(0, -player2.speed)
                elif event.key == py.K_LEFT and player2.x - player2.speed >= 1:
                    player2.move(-player2.speed, 0)
                elif event.key == py.K_DOWN and player2.y - player2.speed <= 9:
                    player2.move(0, player2.speed)
                elif event.key == py.K_RIGHT and player2.x + player2.speed <= 15:
                    player2.move(player2.speed, 0)

        elapsed_time = time.time()
        if elapsed_time >= switch_time:
            bullet_type = not bullet_type
            switch_time = elapsed_time + random.uniform(1, 10)

        elapsed_time1 = int(time.time() - start_time)
        if elapsed_time1 > 3:
            spawn_rate = 0.02
        if elapsed_time1 > 10:
            spawn_rate = 0.03
        if elapsed_time1 > 15:
            spawn_rate = 0.05
        if elapsed_time1 > 25:
            spawn_rate = 0.07

        if random.random() < spawn_rate:
            bullet = Bullet(-BULLET_RADIUS, random.randint(0, HEIGHT), BULLET_SPEED)
            bullets.append(bullet)
        if random.random() < spawn_rate:
            bullet = Bullet(WIDTH + BULLET_RADIUS, random.randint(0, HEIGHT), -BULLET_SPEED)
            bullets.append(bullet)
        for bullet in bullets:
            bullet.move()

        if player1.hp <= 0 or player2.score >= 25:
            winner_text = "Player 2 wins!"
            win = True
        elif player2.hp <= 0 or player1.score >= 25:
            winner_text = "Player 1 wins!"
            win = False

        if winner_text != "":
            bg_music.stop()
            draw_winner(winner_text, win)
            menu()
            break

        check_bullet_collision(bullets, players, bullet_hit_events, blockSize)
        drawGrid(blockSize, players, bullets, bullet_type, elapsed_time1)
    main()

def draw_text(elapsed_time1):
    draw_text = WINNER_FONT.render(str(elapsed_time1), 1, WHITE)
    WIN.blit(draw_text,(WIDTH / 2 - draw_text.get_width() / 2, 10))

def playerDisplay(player, blockSize):
    hitbox_size = 50
    health_sizex = 50
    health_sizey = 10
    empty_x = 50
    empty_y = 10

    health_sizex = (health_sizex / 15) * player.hp

    hitbox = py.Rect(
        (WIDTH // 15) * player.x - blockSize // 2 - hitbox_size // 2,
        (HEIGHT // 10) * player.y - blockSize // 2 - hitbox_size // 2,
        hitbox_size,
        hitbox_size,
    )
    health = py.Rect(
        (WIDTH // 15) * player.x - blockSize // 2 - hitbox_size // 2,
        (HEIGHT // 10) * player.y + blockSize // 2 - hitbox_size // 2,
        health_sizex,
        health_sizey,
    )
    health_empty = py.Rect(
        (WIDTH // 15) * player.x - blockSize // 2 - hitbox_size // 2,
        (HEIGHT // 10) * player.y + blockSize // 2 - hitbox_size // 2,
        empty_x,
        empty_y,
    )

    draw_text = SCORE_FONT.render(str(player.score), 1, WHITE)
    WIN.blit(draw_text,((WIDTH // 15) * player.x - blockSize//1.37,
                        (HEIGHT // 10) * player.y - blockSize*1.7))

    py.draw.rect(WIN, (255, 0, 0), health_empty)
    py.draw.rect(WIN, (0, 255, 0), health)

    # py.draw.rect(WIN, (255, 0, 0), hitbox, 2)
    WIN.blit(player.type, (hitbox.x, hitbox.y))


class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x += self.speed

def check_bullet_collision(bullets, players, bullet_hit_events, blockSize):
    bullets_to_remove = []
    hitbox_size = 50
    for bullet in bullets:
        for player in players:
            if (
                (WIDTH // 15) * player.x - blockSize // 2 - hitbox_size // 2
                < bullet.x
                < (WIDTH // 15) * player.x + blockSize // 4
                and (HEIGHT // 10) * player.y - blockSize // 2 - hitbox_size // 2
                < bullet.y
                < (HEIGHT // 10) * player.y + blockSize // 4
            ):
                py.event.post(py.event.Event(bullet_hit_events[player]))
                bullets_to_remove.append(bullet)

        if bullet.x < 0 or bullet.x > WIDTH:
            bullets_to_remove.append(bullet)

    for bullet in bullets_to_remove:
        try:
            bullets.remove(bullet)
        except:
            pass

def drawGrid(blockSize, players, bullets, bullet_type, elapsed_time1):
    WIN.blit(bg, (0, 0))
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = py.Rect(x, y, blockSize, blockSize)
            py.draw.rect(WIN, BLACK, rect, 1)

    for player in players:
        playerDisplay(player, blockSize)

    for bullet in bullets:
        if bullet_type:
            py.draw.circle(WIN, (255,0,0), (int(bullet.x), int(bullet.y)), BULLET_RADIUS)
        elif bullet_type == False:
            py.draw.circle(WIN, (255,255,0), (int(bullet.x), int(bullet.y)), BULLET_RADIUS)

    draw_text(elapsed_time1)
    py.display.update()

menu()