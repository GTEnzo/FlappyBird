import pygame
import sys

FPS = 60
WIDTH, HEIGHT = 500, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SIZE = (44, 35)
pygame.init()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('data/beginning.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    button_surface = pygame.Surface((200, 50))
    text = font.render("Start", True, BLACK)
    text_rect = text.get_rect(
        center=(button_surface.get_width() / 2,
                button_surface.get_height() / 2))
    button_rect = pygame.Rect(150, 350, 200, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, '#00B8D9', (1, 1, 198, 48))
        else:
            pygame.draw.rect(button_surface, WHITE, (1, 1, 198, 48))
        button_surface.blit(text, text_rect)
        screen.blit(button_surface, (button_rect.x, button_rect.y))
        pygame.display.update()


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
    start_screen()
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
