import pygame
import sys

FPS = 60
WIDTH, HEIGHT = 500, 600
SIZE = (WIDTH, HEIGHT)
BIRD_SIZE = (44, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def start_screen():
    screen.fill((0, 122, 116))
    logo = pygame.transform.scale(pygame.image.load('data/logo.png'), (360, 90))
    screen.blit(logo, (70, 70))

    font = pygame.font.Font(None, 60)
    start_button = pygame.Surface((300, 75))
    text = font.render('Start', True, BLACK)
    text_rect = text.get_rect(
        center=(start_button.get_width() / 2,
                start_button.get_height() / 2))
    start_button_rect = pygame.Rect(100, 220, 300, 75)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    return
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(start_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(start_button, (255, 251, 214), (1, 1, 298, 73))
        start_button.blit(text, text_rect)
        screen.blit(start_button, (start_button_rect.x, start_button_rect.y))
        pygame.display.update()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x = 150
        self.y = 300
        self.gravity = 0.5
        self.jump_strength = -9
        self.velocity = 0
        self.images = [pygame.transform.scale(pygame.image.load(f'data/bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]
        self.shot_image = 0
        self.image = self.images[self.shot_image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 5
        self.time = 0

    def jump(self):
        self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.y = self.y

        if self.y > HEIGHT - 150:
            self.y = HEIGHT - 150
            self.velocity = 0
            self.rect.y = self.y

        self.time += 1
        if self.time >= self.speed:
            self.time = 0
            self.shot_image = (self.shot_image + 1) % len(self.images)
            self.image = self.images[self.shot_image]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    start_screen()
    bird = Bird()
    background = pygame.image.load('data/background.jpg')
    background = pygame.transform.scale(background, SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                bird.jump()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()
        screen.blit(background, (0, 0))
        bird.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
