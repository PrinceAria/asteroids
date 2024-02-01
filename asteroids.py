import pygame
import sys
import math
import random


class AsteroidsGame:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()

        self.player_size = 50
        self.player_x = self.WIDTH // 2
        self.player_y = self.HEIGHT // 2
        self.player_speed = 5
        self.player_angle = 0

        self.bullet_speed = 8
        self.bullets = []

        self.asteroid_speed = 2
        self.asteroids = []

        self.player_score = 0
        self.game_over = False

    def get_player_x(self):
        return self.player_x

    def get_player_y(self):
        return self.player_y

    def get_player_angle(self):
        return self.player_angle

    def get_asteroids(self):
        return self.asteroids

    def get_bullets(self):
        return self.bullets

    def draw_player(self):
        player_points = [
            (self.player_x, self.player_y - self.player_size // 1.5),
            (self.player_x + self.player_size // 2, self.player_y + self.player_size // 2),
            (self.player_x - self.player_size // 2, self.player_y + self.player_size // 2)
        ]
        rotated_points = [
            (
                self.player_x + (point[0] - self.player_x) * math.cos(math.radians(self.player_angle)) - (
                        point[1] - self.player_y) * math.sin(math.radians(self.player_angle)),
                self.player_y + (point[0] - self.player_x) * math.sin(math.radians(self.player_angle)) + (
                        point[1] - self.player_y) * math.cos(math.radians(self.player_angle))
            )
            for point in player_points
        ]

        pygame.draw.polygon(self.screen, self.WHITE, rotated_points)

    def draw_bullets(self):
        for bullet in self.bullets:
            pygame.draw.circle(self.screen, self.WHITE, (int(bullet[0]), int(bullet[1])), 5)

    def draw_asteroids(self):
        for asteroid in self.asteroids:
            pygame.draw.circle(self.screen, self.RED, (int(asteroid[0]), int(asteroid[1])), 20)

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_player_left()
        if keys[pygame.K_RIGHT]:
            self.move_player_right()

        self.player_angle %= 360

        if keys[pygame.K_UP]:
            self.move_player_up()
        if keys[pygame.K_DOWN]:
            self.move_player_down()

        self.player_x = self.player_x % self.WIDTH
        self.player_y = self.player_y % self.HEIGHT

    def move_bullets(self):
        for i in range(len(self.bullets)):
            self.bullets[i][0] += self.bullet_speed * math.cos(math.radians(self.bullets[i][2]))
            self.bullets[i][1] -= self.bullet_speed * math.sin(math.radians(self.bullets[i][2]))

            if self.bullets[i][0] < 0 or self.bullets[i][0] > self.WIDTH or self.bullets[i][1] < 0 or self.bullets[i][
                1] > self.HEIGHT:
                self.bullets.pop(i)
                break

    def move_asteroids(self):
        for i in range(len(self.asteroids)):
            self.asteroids[i][0] += self.asteroid_speed * math.cos(math.radians(self.asteroids[i][2]))
            self.asteroids[i][1] -= self.asteroid_speed * math.sin(math.radians(self.asteroids[i][2]))

            if self.asteroids[i][0] < 0 or self.asteroids[i][0] > self.WIDTH or self.asteroids[i][1] < 0 or \
                    self.asteroids[i][1] > self.HEIGHT:
                self.asteroids.pop(i)
                break

    def reset(self):
        print("Game Over!")
        print(f"Your score: {self.player_score}")
        self.game_over = False
        self.player_x = self.WIDTH // 2
        self.player_y = self.HEIGHT // 2
        self.player_angle = 0
        self.player_score = 0
        self.asteroids.clear()
        self.bullets.clear()

    def render(self):
        self.update()

        pygame.display.flip()
        self.clock.tick()

    def check_collisions(self):
        for asteroid in self.asteroids:
            distance = math.sqrt((self.player_x - asteroid[0]) ** 2 + (self.player_y - asteroid[1]) ** 2)
            if distance < self.player_size / 2 + 20:
                self.game_over = True

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                distance = math.sqrt((bullet[0] - asteroid[0]) ** 2 + (bullet[1] - asteroid[1]) ** 2)
                if distance < 20:
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.player_score += 1
                    break

    def move_player_left(self):
        self.player_angle -= 5

    def move_player_right(self):
        self.player_angle += 5

    def move_player_up(self):
        self.player_x += self.player_speed * math.sin(math.radians(self.player_angle))
        self.player_y -= self.player_speed * math.cos(math.radians(self.player_angle))

    def move_player_down(self):
        self.player_x -= self.player_speed * math.sin(math.radians(self.player_angle))
        self.player_y += self.player_speed * math.cos(math.radians(self.player_angle))

    def shoot_bullet(self):
        self.bullets.append([self.player_x, self.player_y, 90 - self.player_angle])

    def get_collided(self):
        return self.game_over

    def get_score(self):
        return self.player_score

    def spawn_asteroids(self):
        pos_x = random.randint(0, self.WIDTH)
        pos_y = random.randint(0, self.HEIGHT)
        if pos_x not in (self.player_x - 25, self.player_x + 25):
            if pos_y not in (self.player_y - 25, self.player_y + 25):
                (self.asteroids
                 .append([random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT), random.randint(0, 360)]))

    def update(self):
        if not self.game_over:
            self.move_player()
            self.move_bullets()
            self.move_asteroids()
            self.check_collisions()

            self.screen.fill((0, 0, 0))
            self.draw_player()
            self.draw_bullets()
            self.draw_asteroids()

            if random.randint(0, 100) < 4:
                self.spawn_asteroids()

            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(self.player_score), True, self.WHITE)
            self.screen.blit(text, (10, 10))
        else:
            self.reset()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shoot_bullet()

            self.update()

            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(self.player_score), True, self.WHITE)
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            self.clock.tick(self.FPS)


# Instantiate the AsteroidsGame class and run the game
if __name__ == '__main__':
    asteroids_game = AsteroidsGame()
    asteroids_game.run_game()
