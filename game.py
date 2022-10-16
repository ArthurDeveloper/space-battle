import pygame

class Ship:
    def __init__(self):
        self.image = pygame.image.load('res/ship.png')

    def draw(self, screen):
        screen.blit(self.image, (150, 100))


screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Space Battle!')

ship = Ship()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0, 255))

    ship.draw(screen)

    pygame.display.flip()


