import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('sansserif', 50)
WINNER_FONT = pygame.font.SysFont('sansserif', 90)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
TANK_WIDTH, TANK_HEIGHT = 60, 50

TANK1_HIT = pygame.USEREVENT + 1
TANK2_HIT = pygame.USEREVENT + 2

tank1_path = "C:/Users/ASUS/PycharmProjects/assets/tank1.png"
TANK1 = pygame.image.load(tank1_path)
TANK1 = pygame.transform.rotate(pygame.transform.scale(TANK1,(TANK_WIDTH,TANK_HEIGHT)),270)
tank2_path = "C:/Users/ASUS/PycharmProjects/assets/tank2.png"
TANK2 = pygame.image.load(tank2_path)
TANK2 = pygame.transform.rotate(pygame.transform.scale(TANK2,(TANK_WIDTH,TANK_HEIGHT)),90)
battleground_path = "C:/Users/ASUS/PycharmProjects/assets/battleground.png"
BATTLEGROUND = pygame.image.load(battleground_path)
BATTLEGROUND = pygame.transform.scale(BATTLEGROUND,(WIDTH,HEIGHT))

def draw_window(red, yellow, tank2_bullets, tank1_bullets, tank2_health, tank1_health):
    WIN.blit(BATTLEGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    tank2_health_text = HEALTH_FONT.render(
        "Health: " + str(tank2_health), 1, WHITE)
    tank1_health_text = HEALTH_FONT.render(
        "Health: " + str(tank1_health), 1, WHITE)
    WIN.blit(tank2_health_text, (WIDTH - tank2_health_text.get_width() - 10, 10))
    WIN.blit(tank1_health_text, (10, 10))

    WIN.blit(TANK1, (yellow.x, yellow.y))
    WIN.blit(TANK2, (red.x, red.y))

    for bullet in tank2_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in tank1_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(tank1_bullets, tank2_bullets, yellow, red):
    for bullet in tank1_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TANK2_HIT))
            tank1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            tank1_bullets.remove(bullet)

    for bullet in tank2_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TANK1_HIT))
            tank2_bullets.remove(bullet)
        elif bullet.x < 0:
            tank2_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, TANK_WIDTH, TANK_HEIGHT)
    yellow = pygame.Rect(100, 300, TANK_WIDTH, TANK_HEIGHT)

    tank2_bullets = []
    tank1_bullets = []

    tank2_health = 10
    tank1_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(tank1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    tank1_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(tank2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    tank2_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == TANK2_HIT:
                tank2_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == TANK1_HIT:
                tank1_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if tank2_health <= 0:
            winner_text = "PLAYER1 Wins!"

        if tank1_health <= 0:
            winner_text = "PLAYER2 Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(tank1_bullets, tank2_bullets, yellow, red)

        draw_window(red, yellow, tank2_bullets, tank1_bullets,
                    tank2_health, tank1_health)




if __name__ == "__main__":
    main()


