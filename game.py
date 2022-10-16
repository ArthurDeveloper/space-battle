import pygame

class Ship:
    def __init__(self):
        self.x = 10
        self.y = 150

        self.speed = 250
        self.direction = 1

        self.image = pygame.image.load('res/ship.png')
        size_x, size_y = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (size_x/2.5, size_y/2.5))

    def spawn_bullet(self):
        size_x, size_y = self.image.get_size()
        new_bullet = Bullet(self.x + size_x - 20, self.y + size_y - 10)
        return new_bullet

    def update(self, delta):
        self.y += self.speed * self.direction * delta

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 500

    def update(self, delta):
        self.x += 500 * delta

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 50, 10))


screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Battle!')

ship = Ship()
bullets = []

clock = pygame.time.Clock()

running = True
while running:
    delta = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                ship.direction = -1

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                ship.direction = 1

            if event.key == pygame.K_RETURN:
                new_bullet = ship.spawn_bullet()
                bullets.append(new_bullet)

    screen.fill((0, 0, 0, 255))

    ship.update(delta)
    ship.draw(screen)
    for bullet in bullets:
        bullet.update(delta)
        bullet.draw(screen)
        if bullet.x > 800:
            bullets.remove(bullets.index(bullet))

    pygame.display.flip()


