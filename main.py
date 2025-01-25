import pygame
import sys
import os

FPS = 60
WIDTH, HEIGHT = 500, 600
SIZE = (WIDTH, HEIGHT)
BIRD_SIZE = (44, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    image = load_image('logo.png')
    screen.fill((0, 122, 116))
    logo = pygame.transform.scale(image, (360, 90))
    screen.blit(logo, (70, 70))

    font = pygame.font.Font(None, 60)
    start_button = pygame.Surface((300, 75))
    text = font.render('Start', True, BLACK)
    text_rect = text.get_rect(
        center=(start_button.get_width() / 2,
                start_button.get_height() / 2))
    start_button_rect = pygame.Rect(100, 220, 300, 75)

    leaders_button = pygame.Surface((300, 75))
    leaders_text = font.render('Leaders', True, BLACK)
    leaders_text_rect = leaders_text.get_rect(
        center=(leaders_button.get_width() / 2,
                leaders_button.get_height() / 2))
    leaders = pygame.Rect(100, 320, 300, 75)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    return
                if leaders.collidepoint(event.pos):
                    leaders_window()

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(start_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(start_button, (255, 251, 214), (1, 1, 298, 73))
        start_button.blit(text, text_rect)
        screen.blit(start_button, (start_button_rect.x, start_button_rect.y))

        if leaders.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(leaders_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(leaders_button, (255, 251, 214), (1, 1, 298, 73))
        leaders_button.blit(leaders_text, leaders_text_rect)
        screen.blit(leaders_button, (leaders.x, leaders.y))

        pygame.display.update()


def leaders_window():
    window = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Leaders")
    window.fill((0, 122, 116))

    font = pygame.font.Font(None, 40)
    back_button = pygame.Surface((152, 50))
    back_text = font.render('Back', True, BLACK)
    back_text_rect = back_text.get_rect(center=(back_button.get_width() / 2, back_button.get_height() / 2))
    back_button_rect = pygame.Rect(5, 5, 152, 50)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    waiting = False

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(back_button, (141, 199, 63), (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, (255, 251, 214), (1, 1, 150, 48))
        back_button.blit(back_text, back_text_rect)
        window.blit(back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.flip()

    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    screen.fill((0, 122, 116))
    logo = pygame.transform.scale(pygame.image.load('data/logo.png'), (360, 90))
    screen.blit(logo, (70, 70))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x = 150
        self.y = 300
        self.gravity = 0.5
        self.jump_strength = -9
        self.velocity = 0
        self.images = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]
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


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('ground.jpg')
        self.speed = 2
        self.x = 0

    def update(self):
        self.x -= self.speed
        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 485))
        if self.x < 0:
            screen.blit(self.image, (self.x + 500, 485))


if __name__ == '__main__':
    start_screen()
    bird = Bird()
    ground = Ground()
    background = load_image('background.jpg')
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
        ground.update()
        screen.blit(background, (0, 0))
        bird.draw(screen)
        ground.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
