import pygame
import random

pygame.init()

debug_mode = False

class Ship:
    def __init__(self):
        self.x = 10
        self.y = 150

        self.speed = 250
        self.direction = 1

        self.score = 0
        with open('high-score.txt', 'a+') as file:
            try:
                self.high_score = int(file.readline())
            except:
                self.high_score = 0

        self.image = pygame.image.load('res/ship.png')
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (size_x/2.5, size_y/2.5))

        self.hitbox = pygame.Rect(self.x, self.y, size_x/2.5, size_y/2.5)

    def spawn_bullet(self):
        size_x, size_y = self.image.get_size()
        new_bullet = Bullet(self.x + size_x - 20, self.y + size_y - 10)
        return new_bullet

    def update(self, delta):
        if not player_has_died:
            self.y += self.speed * self.direction * delta
            self.hitbox.y = self.y

    def draw(self, screen):
        if debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 500
        
        self.rect = pygame.Rect((self.x, self.y, 50, 10))

    def update(self, delta):
        if not player_has_died:
            self.x += 500 * delta

        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)


class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 300

        self.image = pygame.image.load('res/monster.png')
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (size_x/2.5, size_y/2.5))

        self.hitbox = pygame.Rect(self.x, self.y, size_x/2.5, size_y/2.5)

    def update(self, delta):
        if not player_has_died:
            self.x -= self.speed * delta
            self.hitbox.x = self.x

    def draw(self, screen):
        if debug_mode:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox)
        screen.blit(self.image, (self.x, self.y))


screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Battle!')

ship = Ship()
bullets = []
monsters = []
monster_spawn_time = random.uniform(0.2, 3)
timer = 0
score_text_color = (255, 255, 255)
high_score_text_color = (255, 255, 255)

clock = pygame.time.Clock()

running = True
player_has_died = False
while running:
    delta = clock.tick(60) / 1000

    timer += delta


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                ship.direction = -1

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                ship.direction = 1

            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if player_has_died:
                    player_has_died = False
                    monsters.clear()
                    ship.y = 100
                    ship.score = 0
                    high_score_text_color = (255, 255, 255)
                    continue

                new_bullet = ship.spawn_bullet()
                bullets.append(new_bullet)

    screen.fill((0, 0, 0, 255))

    ship.update(delta)
    ship.draw(screen)
    for bullet in bullets:
        bullet.update(delta)
        bullet.draw(screen)
        if bullet.x > 800:
            bullets.remove(bullet)

        for monster in monsters:
            if bullet.rect.colliderect(monster.hitbox):
                monsters.remove(monster)
                bullets.remove(bullet)
                ship.score += 500
                score_text_color = (0, 255, 0)

    for monster in monsters:
        monster.update(delta)
        monster.draw(screen)
        if monster.x < -200:
            monsters.remove(monster)
            ship.score -= 200
            score_text_color = (255, 0, 0)

        if monster.hitbox.colliderect(ship.hitbox):
            if player_has_died:
                monsters.remove(monster)
            else:
                player_has_died = True
                if ship.score > ship.high_score:
                    with open('high-score.txt', 'w') as file:
                        file.write(str(ship.score))
                        ship.high_score = ship.score
                        high_score_text_color = (0, 255, 0)

    if timer > monster_spawn_time and not player_has_died:
        monster_spawn_time = random.uniform(0.2, 3)
        timer = 0

        new_monster = Monster(900, random.randint(0, 600))
        monsters.append(new_monster)

    if player_has_died:
        font = pygame.font.SysFont('Arial', 128)
        
        you_died_text = font.render('YOU DIED!', True, (255, 0, 0))
        text_rect = you_died_text.get_rect()
        screen.blit(you_died_text, (800/2 - text_rect.w/2, 600/2 - text_rect.h/2 - 150))

        font = pygame.font.SysFont('Arial', 32)
        restart_instructions_text = font.render('Press Enter or Spacebar to restart', True, (255, 0, 0))
        text_rect = restart_instructions_text.get_rect()
        screen.blit(restart_instructions_text, (800/2 - text_rect.w/2, 600/2 + text_rect.h/2))

        if ship.score == ship.high_score:
            font = pygame.font.SysFont('Arial', 24)
            high_score_text = font.render('NEW HIGH SCORE! ' + str(ship.high_score), True, (0, 255, 0))
            text_rect = high_score_text.get_rect()
            screen.blit(high_score_text, (800/2 - text_rect.w/2, 600/2 + text_rect.h/2 + 100))

    font = pygame.font.SysFont('Arial', 32)
    ship_score_text = font.render('Score: '+str(ship.score), True, score_text_color)
    screen.blit(ship_score_text, (20, 20))

    ship_high_score_text = font.render('Hi: '+str(ship.high_score), True, high_score_text_color)
    screen.blit(ship_high_score_text, (20, 60))

    pygame.display.flip()
 

