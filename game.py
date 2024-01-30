import pygame
import sys
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
player_angle = 0

bullet_speed = 8
bullets = []

asteroid_speed = 2
asteroids = []

player_score = 0


def draw_player(x, y, angle):
    player_points = [
        (x, y - player_size // 1.5),
        (x + player_size // 2, y + player_size // 2),
        (x - player_size // 2, y + player_size // 2)
    ]
    rotated_points = [
        (
            x + (point[0] - x) * math.cos(math.radians(angle)) - (point[1] - y) * math.sin(math.radians(angle)),
            y + (point[0] - x) * math.sin(math.radians(angle)) + (point[1] - y) * math.cos(math.radians(angle))
        )
        for point in player_points
    ]

    pygame.draw.polygon(screen, WHITE, rotated_points)


def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)


def draw_asteroids(asteroids):
    for asteroid in asteroids:
        pygame.draw.circle(screen, RED, (int(asteroid[0]), int(asteroid[1])), 20)


def move_player():
    global player_x, player_y, player_angle

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle += 5
    if keys[pygame.K_RIGHT]:
        player_angle -= 5

    player_angle %= 360

    angle_radians = math.radians(player_angle)
    if (keys[pygame.K_UP]):
        player_x += player_speed * math.sin(angle_radians)
        player_y -= player_speed * math.cos(angle_radians)
    if (keys[pygame.K_DOWN]):
        player_x -= player_speed * math.sin(angle_radians)
        player_y += player_speed * math.cos(angle_radians)

    player_x = player_x % WIDTH
    player_y = player_y % HEIGHT


def move_bullets(bullets):
    for i in range(len(bullets)):
        bullets[i][0] += bullet_speed * math.cos(math.radians(bullets[i][2]))
        bullets[i][1] -= bullet_speed * math.sin(math.radians(bullets[i][2]))

        if bullets[i][0] < 0 or bullets[i][0] > WIDTH or bullets[i][1] < 0 or bullets[i][1] > HEIGHT:
            bullets.pop(i)
            break


def move_asteroids(asteroids):
    for i in range(len(asteroids)):
        asteroids[i][0] += asteroid_speed * math.cos(math.radians(asteroids[i][2]))
        asteroids[i][1] -= asteroid_speed * math.sin(math.radians(asteroids[i][2]))

        if asteroids[i][0] < 0 or asteroids[i][0] > WIDTH or asteroids[i][1] < 0 or asteroids[i][1] > HEIGHT:
            asteroids.pop(i)
            break


def check_collisions():
    global player_x, player_y, player_size, asteroids, bullets, player_score

    for asteroid in asteroids:
        distance = math.sqrt((player_x - asteroid[0]) ** 2 + (player_y - asteroid[1]) ** 2)
        if distance < player_size / 2 + 20:
            print("Game Over!")
            pygame.quit()
            sys.exit()

    for bullet in bullets:
        for asteroid in asteroids:
            distance = math.sqrt((bullet[0] - asteroid[0]) ** 2 + (bullet[1] - asteroid[1]) ** 2)
            if distance < 20:
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                player_score += 1
                break


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x, player_y, 90 - player_angle])

    move_player()

    move_bullets(bullets)

    move_asteroids(asteroids)

    check_collisions()

    screen.fill((0, 0, 0))
    draw_player(player_x, player_y, player_angle)
    draw_bullets(bullets)
    draw_asteroids(asteroids)

    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(player_score), True, WHITE)
    screen.blit(text, (10, 10))

    if random.randint(0, 100) < 2:
        asteroids.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(0, 360)])

    pygame.display.flip()
    clock.tick(FPS)
