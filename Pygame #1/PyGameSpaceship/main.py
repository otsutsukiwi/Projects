import pygame as py
import time

py.font.init()
py.mixer.init()

WIDTH, HEIGHT = 700, 900
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Bad Orange")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BLACK_RECT = py.Rect(0, 0, WIDTH, HEIGHT / 2)
SEP_RECT = py.Rect(0, HEIGHT // 2 - 2, WIDTH, 4)

FPS = 60
BULLET_VEL = 8
BIG_BULLET_VEL = 2
SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT = 90, 60

WHITE_HIT = py.USEREVENT + 1
BLACK_HIT = py.USEREVENT + 2

icon_surface = py.image.load(
    "PyGameSpaceship\Assets\Bad Orange.png"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
py.display.set_icon(icon_surface)

MUSIC = py.mixer.Sound(
    "PyGameSpaceship\Assets\\11. Night of Nights.mp3"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
BULLET_HIT = py.mixer.Sound(
    "PyGameSpaceship\Assets\explosion - Creator Marketplace.ogg"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
BULLET_SHOOT = py.mixer.Sound(
    "PyGameSpaceship\Assets\Laser Shot.ogg"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
BULLET_HIT.set_volume(0.5)
BULLET_SHOOT.set_volume(0.5)

HEALTH_FONT = py.font.SysFont("freesansbold", 40)
WINNER_FONT = py.font.SysFont("freesansbold", 70)

BLACK_SPACESHIP_IMAGE = py.image.load(
    "PyGameSpaceship\Assets\\black_ship.png"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
BLACK_SPACESHIP = py.transform.rotate(
    py.transform.scale(BLACK_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 0
)

WHITE_SPACESHIP_IMAGE = py.image.load(
    "PyGameSpaceship\Assets\white_ship.png"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
WHITE_SPACESHIP = py.transform.rotate(
    py.transform.scale(WHITE_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)),
    180,
)

BG_IMAGE_LOAD = py.image.load(
    "PyGameSpaceship\Assets\\bad_orange.png"
)  # CHANGE THESE DIRECTORIES IF THEY DO NOT WORK
BG_IMAGE = py.transform.scale(BG_IMAGE_LOAD, (WIDTH + 200, HEIGHT + 0))


def draw_window(
    white,
    black,
    white_bullets,
    black_bullets,
    white_hp,
    black_hp,
    white_big,
    black_big,
    time,
):
    WIN.fill(WHITE)
    WIN.blit(BG_IMAGE, (-100, -21))

    if time > 20:
        top_time_text = WINNER_FONT.render(str(time), 1, RED)
        WIN.blit(
            top_time_text,
            (
                WIDTH - top_time_text.get_width() - 80,
                HEIGHT // 2 - top_time_text.get_height(),
            ),
        )
        bot_time_text = WINNER_FONT.render(str(time), 1, RED)
        WIN.blit(bot_time_text, (80, HEIGHT // 2 + 10))
    else:
        top_time_text = HEALTH_FONT.render(str(time), 1, WHITE)
        WIN.blit(
            top_time_text,
            (
                WIDTH - top_time_text.get_width() - 80,
                HEIGHT // 2 - top_time_text.get_height(),
            ),
        )
        bot_time_text = HEALTH_FONT.render(str(time), 1, BLACK)
        WIN.blit(bot_time_text, (80, HEIGHT // 2 + 10))

    white_hp_text = HEALTH_FONT.render("Health: " + str(white_hp), 1, BLACK)
    black_hp_text = HEALTH_FONT.render("Health: " + str(black_hp), 1, WHITE)
    WIN.blit(
        white_hp_text,
        (
            WIDTH // 2 - white_hp_text.get_width() / 2,
            HEIGHT // 2 - white_hp_text.get_height() / 2 - 20,
        ),
    )
    WIN.blit(
        black_hp_text,
        (
            WIDTH // 2 - white_hp_text.get_width() / 2,
            HEIGHT // 2 - white_hp_text.get_height() / 2 + 20,
        ),
    )

    controls_white_text_WASD = HEALTH_FONT.render("WASD - move", 1, WHITE)
    WIN.blit(controls_white_text_WASD, (10, 10))
    controls_white_text_SHOOT = HEALTH_FONT.render("f - bullet", 1, WHITE)
    WIN.blit(
        controls_white_text_SHOOT, (10, controls_white_text_WASD.get_height() + 10)
    )
    controls_white_text_BIG = HEALTH_FONT.render("g - big bullet", 1, WHITE)
    WIN.blit(
        controls_white_text_BIG,
        (
            10,
            controls_white_text_WASD.get_height()
            + controls_white_text_SHOOT.get_height()
            + 10,
        ),
    )
    controls_white_text_BOOST = HEALTH_FONT.render("h - boost", 1, WHITE)
    WIN.blit(
        controls_white_text_BOOST,
        (
            10,
            controls_white_text_WASD.get_height()
            + controls_white_text_SHOOT.get_height()
            + controls_white_text_BIG.get_height()
            + 10,
        ),
    )

    controls_black_text_BOOST = HEALTH_FONT.render("i - boost", 1, BLACK)
    WIN.blit(
        controls_black_text_BOOST,
        (
            WIDTH - controls_black_text_BOOST.get_width() - 10,
            HEIGHT - controls_black_text_BOOST.get_height() - 10,
        ),
    )
    controls_black_text_BIG = HEALTH_FONT.render("p - big bullet", 1, BLACK)
    WIN.blit(
        controls_black_text_BIG,
        (
            WIDTH - controls_black_text_BIG.get_width() - 10,
            HEIGHT
            - controls_black_text_BOOST.get_height()
            - controls_black_text_BIG.get_height()
            - 10,
        ),
    )
    controls_black_text_SHOOT = HEALTH_FONT.render("o - bullet", 1, BLACK)
    WIN.blit(
        controls_black_text_SHOOT,
        (
            WIDTH - controls_black_text_SHOOT.get_width() - 10,
            HEIGHT
            - controls_black_text_BOOST.get_height()
            - controls_black_text_BIG.get_height()
            - controls_black_text_SHOOT.get_height()
            - 10,
        ),
    )
    controls_black_text_ARROW = HEALTH_FONT.render("ARROW KEYS - move", 1, BLACK)
    WIN.blit(
        controls_black_text_ARROW,
        (
            WIDTH - controls_black_text_ARROW.get_width() - 10,
            HEIGHT
            - controls_black_text_BOOST.get_height()
            - controls_black_text_BIG.get_height()
            - controls_black_text_SHOOT.get_height()
            - controls_black_text_ARROW.get_height()
            - 10,
        ),
    )

    py.draw.rect(WIN, BLACK, SEP_RECT)
    WIN.blit(BLACK_SPACESHIP, (black.x, black.y))
    WIN.blit(WHITE_SPACESHIP, (white.x, white.y))

    for bullet in white_bullets:
        border_width = 1
        py.draw.rect(WIN, WHITE, bullet)
        py.draw.rect(WIN, BLACK, bullet, border_width)

    for bullet in black_bullets:
        border_width = 1
        py.draw.rect(WIN, BLACK, bullet)
        py.draw.rect(WIN, WHITE, bullet, border_width)

    for bullet in white_big:
        border_width = 1
        py.draw.rect(WIN, WHITE, bullet)
        py.draw.rect(WIN, BLACK, bullet, border_width)

    for bullet in black_big:
        border_width = 1
        py.draw.rect(WIN, BLACK, bullet)
        py.draw.rect(WIN, WHITE, bullet, border_width)

    py.display.update()


def white_movement(keys_pressed, white):
    VEL = 5
    if keys_pressed[py.K_h]:
        VEL += 5
        if keys_pressed[py.K_a] and white.x - VEL > 0:  # LEFT
            white.x -= VEL
        if keys_pressed[py.K_d] and white.x + VEL + white.width < WIDTH:  # RIGHT
            white.x += VEL
        if keys_pressed[py.K_w] and white.y - VEL > 0:  # UP
            white.y -= VEL
        if keys_pressed[py.K_s] and white.y + VEL + white.height < SEP_RECT.y:  # DOWN
            white.y += VEL
    else:
        if keys_pressed[py.K_a] and white.x - VEL > 0:  # LEFT
            white.x -= VEL
        if keys_pressed[py.K_d] and white.x + VEL + white.width < WIDTH:  # RIGHT
            white.x += VEL
        if keys_pressed[py.K_w] and white.y - VEL > 0:  # UP
            white.y -= VEL
        if keys_pressed[py.K_s] and white.y + VEL + white.height < SEP_RECT.y:  # DOWN
            white.y += VEL


def black_movement(keys_pressed, black):
    VEL = 5
    if keys_pressed[py.K_i]:
        VEL += 5
        if keys_pressed[py.K_LEFT] and black.x - VEL > 0:  # LEFT
            black.x -= VEL
        if keys_pressed[py.K_RIGHT] and black.x + VEL + black.width < WIDTH:  # RIGHT
            black.x += VEL
        if keys_pressed[py.K_UP] and black.y + VEL - 10 > SEP_RECT.y:  # UP
            black.y -= VEL
        if keys_pressed[py.K_DOWN] and black.y + VEL + black.height < HEIGHT:  # DOWN
            black.y += VEL
    else:
        if keys_pressed[py.K_LEFT] and black.x - VEL > 0:  # LEFT
            black.x -= VEL
        if keys_pressed[py.K_RIGHT] and black.x + VEL + black.width < WIDTH:  # RIGHT
            black.x += VEL
        if keys_pressed[py.K_UP] and black.y + VEL - 10 > SEP_RECT.y:  # UP
            black.y -= VEL
        if keys_pressed[py.K_DOWN] and black.y + VEL + black.height < HEIGHT:  # DOWN
            black.y += VEL


def handle_bullets(white_bullets, black_bullets, white, black, white_big, black_big):
    for bullet in white_bullets:
        bullet.y += BULLET_VEL
        if black.colliderect(bullet):
            py.event.post(py.event.Event(BLACK_HIT))
            white_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            white_bullets.remove(bullet)

    for bullet in black_bullets:
        bullet.y -= BULLET_VEL
        if white.colliderect(bullet):
            py.event.post(py.event.Event(WHITE_HIT))
            black_bullets.remove(bullet)
        elif bullet.y < 0:
            black_bullets.remove(bullet)

    for bullet in white_big:
        bullet.height += 1
        bullet.y += BIG_BULLET_VEL
        if black.colliderect(bullet):
            py.event.post(py.event.Event(BLACK_HIT))
            white_big.remove(bullet)
        elif bullet.y > HEIGHT:
            white_big.remove(bullet)

    for bullet in black_big:
        bullet.height += 1
        bullet.y -= BIG_BULLET_VEL + 1
        if white.colliderect(bullet):
            py.event.post(py.event.Event(BLACK_HIT))
            black_big.remove(bullet)
        elif bullet.y + bullet.height < 0:
            black_big.remove(bullet)


def draw_winner(text, win):
    if win:
        draw_text = WINNER_FONT.render(text, 1, BLACK)
        WIN.blit(
            draw_text,
            (
                WIDTH / 2 - draw_text.get_width() / 2,
                draw_text.get_height() / 2 + HEIGHT - 100,
            ),
        )
        py.display.update()
        py.time.delay(2000)
    else:
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(
            draw_text,
            (WIDTH / 2 - draw_text.get_width() / 2, draw_text.get_height() / 2),
        )
        py.display.update()
        py.time.delay(2000)


def main():
    MUSIC.play()
    win = None
    white_hp = 5
    black_hp = 5
    winner_text = ""

    MUSIC.set_volume(0.05)

    MAX_BULLETS = 3
    MAX_BIG_BULLETS = 1

    white = py.Rect((WIDTH / 4 * 3) - 60, 150, SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)
    black = py.Rect(
        (WIDTH / 4) - 30,
        HEIGHT - SPACE_SHIP_HEIGHT - 150,
        SPACE_SHIP_WIDTH,
        SPACE_SHIP_HEIGHT,
    )

    white_bullets = []
    white_big = []
    black_bullets = []
    black_big = []

    start_time = time.time()
    clock = py.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        elapsed_time = int(time.time() - start_time)
        if elapsed_time > 20:
            MAX_BULLETS = 5
            MAX_BIG_BULLETS = 3
            MUSIC.set_volume(0.15)

        keys_pressed = py.key.get_pressed()
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()

            if event.type == py.KEYDOWN:
                if (
                    event.key == py.K_f
                    and len(white_bullets) < MAX_BULLETS
                    and not keys_pressed[py.K_h]
                ):
                    bullet = py.Rect(
                        white.x + white.width // 2 - 2, white.y + white.height, 5, 15
                    )
                    white_bullets.append(bullet)
                    BULLET_SHOOT.play()

                if (
                    event.key == py.K_g
                    and len(white_big) < MAX_BIG_BULLETS
                    and not keys_pressed[py.K_h]
                ):
                    bullet = py.Rect(
                        white.x + white.width // 2 - 12, white.y + white.height, 25, 25
                    )
                    white_big.append(bullet)
                    BULLET_SHOOT.play()

                if (
                    event.key == py.K_o
                    and len(black_bullets) < MAX_BULLETS
                    and not keys_pressed[py.K_i]
                ):
                    bullet = py.Rect(black.x + black.width // 2 - 2, black.y - 5, 5, 15)
                    black_bullets.append(bullet)
                    BULLET_SHOOT.play()

                if (
                    event.key == py.K_p
                    and len(black_big) < MAX_BIG_BULLETS
                    and not keys_pressed[py.K_i]
                ):
                    bullet = py.Rect(black.x + black.width // 2 - 12, black.y, 25, 25)
                    black_big.append(bullet)
                    BULLET_SHOOT.play()
            if event.type == WHITE_HIT:
                white_hp -= 1
                BULLET_HIT.play()
            if event.type == BLACK_HIT:
                black_hp -= 1
                BULLET_HIT.play()
        if white_hp <= 0:
            winner_text = "Black Wins!"
            win = True
        if black_hp <= 0:
            winner_text = "White Wins!"
            win = False

        if winner_text != "":
            draw_winner(winner_text, win)
            MUSIC.set_volume(0.05)
            MUSIC.stop()
            break

        white_movement(keys_pressed, white)
        black_movement(keys_pressed, black)

        handle_bullets(white_bullets, black_bullets, white, black, white_big, black_big)

        draw_window(
            white,
            black,
            white_bullets,
            black_bullets,
            white_hp,
            black_hp,
            white_big,
            black_big,
            elapsed_time,
        )
    main()


if __name__ == "__main__":
    main()
