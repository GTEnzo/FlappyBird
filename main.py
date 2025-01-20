import pygame
import sys

WIDTH, HEIGHT = 500, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SIZE = (44, 35)
pygame.init()
all_sprites = pygame.sprite.Group()


def start():
    beginning = pygame.transform.scale(pygame.image.load('data/beginning.jpg'), (WIDTH, HEIGHT))
    screen.blit(beginning, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


class Bird(pygame.sprite.Sprite):
    bird_img = pygame.image.load('data/bird.png')
    bird_img = pygame.transform.scale(bird_img, SIZE)

    def __init__(self):
        super().__init__(all_sprites)
        self.x = 150
        self.y = 300
        self.gravity = 0.5
        self.jump_strength = -9
        self.velocity_y = 0

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y > HEIGHT - 83:
            self.y = HEIGHT - 83
            self.velocity_y = 0

    def draw(self, screen):
        screen.blit(self.bird_img, (self.x, self.y))


if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    start()
    bird = Bird()
    back_img = pygame.image.load('data/background.jpg')
    back_img = pygame.transform.scale(back_img, (500, 600))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                bird.jump()
            if event.type == pygame.K_SPACE or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                bird.jump()
        bird.update()
        screen.blit(back_img, (0, 0))
        bird.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
