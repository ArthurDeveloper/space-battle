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

    def update(self, delta):
        self.y += self.speed * self.direction * delta

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Battle!')

ship = Ship()

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


    screen.fill((0, 0, 0, 255))

    ship.update(delta)
    ship.draw(screen)

    pygame.display.flip()


