import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Bird:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.jump_strength = -10
        self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))


bird = Bird(50, HEIGHT // 2, 30, 30)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            bird.jump()
    bird.update()
    screen.fill(WHITE)
    bird.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
