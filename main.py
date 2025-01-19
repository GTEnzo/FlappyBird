import pygame
import sys

WIDTH, HEIGHT = 500, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Bird:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.width = 44
        self.height = 35
        self.bird_img = pygame.image.load('bird.png').convert_alpha()
        self.bird_img = pygame.transform.scale(self.bird_img, (self.width, self.height))
        self.gravity = 0.5
        self.jump_strength = -9
        self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity_y = 0

    def draw(self, screen):
        screen.blit(self.bird_img, (self.x, self.y))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    bird = Bird()
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
