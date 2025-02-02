import pygame
import random
import sys
import csv
import os

FPS = 60
WIDTH, HEIGHT = 450, 600
SIZE = (WIDTH, HEIGHT)
BIRD_SIZE = (45, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

score = 0

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Flappy Bird')
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
    screen.fill((0, 122, 116))

    image = load_image('logo.png')
    logo = pygame.transform.scale(image, (360, 90))
    screen.blit(logo, (45, 45))

    font = pygame.font.Font(None, 60)

    start_button = pygame.Surface((300, 75))
    start_text = font.render('Start', True, BLACK)
    start_rect = start_text.get_rect(
        center=(start_button.get_width() / 2,
                start_button.get_height() / 2))
    start_button_rect = pygame.Rect(75, 220, 300, 75)

    leaders_button = pygame.Surface((300, 75))
    leaders_text = font.render('Leaders', True, BLACK)
    leaders_rect = leaders_text.get_rect(
        center=(leaders_button.get_width() / 2,
                leaders_button.get_height() / 2))
    leaders_button_rect = pygame.Rect(75, 320, 300, 75)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    return
                if leaders_button_rect.collidepoint(event.pos):
                    leaders_window()

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(start_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(start_button, (255, 251, 214), (1, 1, 298, 73))
        start_button.blit(start_text, start_rect)
        screen.blit(start_button, (start_button_rect.x, start_button_rect.y))

        if leaders_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(leaders_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(leaders_button, (255, 251, 214), (1, 1, 298, 73))
        leaders_button.blit(leaders_text, leaders_rect)
        screen.blit(leaders_button, (leaders_button_rect.x, leaders_button_rect.y))

        pygame.display.update()


def leaders_window():
    window = pygame.display.set_mode(SIZE)
    window.fill((0, 122, 116))

    with open('leaderboard.csv', encoding="utf8") as csvfile:
        file = csv.reader(csvfile, delimiter=';', quotechar='"')
        leaders = []

        for index, row in enumerate(file):
            if index > 10:
                break
            leaders.append(row)

    font = pygame.font.Font(None, 40)

    y = 100
    place = 1
    for i in leaders[1:]:
        name = font.render(f'{place}. {i[0]}:', True, WHITE)
        screen.blit(name, (100, y))

        points = font.render(f'{i[1]}', True, WHITE)
        screen.blit(points, (300, y))

        y += 40
        place += 1

    back_button = pygame.Surface((152, 50))
    back_text = font.render('Back', True, BLACK)
    back_rect = back_text.get_rect(
        center=(back_button.get_width() / 2,
                back_button.get_height() / 2))
    back_button_rect = pygame.Rect(5, 5, 152, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    running = False

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(back_button, (141, 199, 63), (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, (255, 251, 214), (1, 1, 150, 48))
        back_button.blit(back_text, back_rect)
        window.blit(back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.update()

    start_screen()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.x = 150
        self.y = 300
        self.gravity = 0.6
        self.jump_strength = -9
        self.boost = 0
        self.images = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]
        self.shot = 0
        self.image = self.images[self.shot]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.shots = 5
        self.num = 0

    def jump(self):
        self.boost = self.jump_strength

    def update(self):
        self.boost += self.gravity
        self.y += self.boost
        self.rect.y = self.y

        if self.y > HEIGHT - 150:
            self.y = HEIGHT - 150
            self.boost = 0
            self.rect.y = self.y

        self.num += 1
        if self.num >= self.shots:
            self.num = 0
            self.shot = (self.shot + 1) % len(self.images)
            self.image = self.images[self.shot]

        if self.boost < 0:
            self.image = pygame.transform.rotate(self.images[self.shot], min(25, max(0, -self.boost * 4)))
        elif self.boost > 0:
            self.image = pygame.transform.rotate(self.images[self.shot], max(-70, min(0, self.boost * -8)))
        else:
            self.image = self.images[self.shot]

        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image1 = load_image('pipe1.png')
        self.image2 = load_image('pipe2.png')
        self.x1 = 700
        self.x2 = 950
        self.scrolling = 2
        self.random_y1 = random.randint(200, 460)
        self.y1 = self.random_y1 - 1000
        self.random_y2 = random.randint(200, 460)
        self.y2 = self.random_y2 - 1000

    def update(self):
        self.x1 -= self.scrolling
        self.x2 -= self.scrolling

        if self.x1 == 150 or self.x2 == 150:
            self.score()

        if self.x1 <= -WIDTH:
            self.x1 = 0
        if self.x2 <= -WIDTH:
            self.x2 = 0

    def score(self):
        global score

        score += 1

    def draw(self, screen):
        global score

        screen.blit(self.image1, (self.x1, self.random_y1))
        screen.blit(self.image2, (self.x1, self.y1))
        screen.blit(self.image1, (self.x2, self.random_y2))
        screen.blit(self.image2, (self.x2, self.y2))

        if self.x1 < -50:
            self.random_y1 = random.randint(200, 460)
            self.y1 = self.random_y1 - 1000

            if score > 38:
                self.y1 += 30
            elif score > 18:
                self.y1 += 15

            self.x1 = 450
            screen.blit(self.image1, (self.x1, self.random_y1))
            screen.blit(self.image2, (self.x1, self.y1))

        if self.x2 < -50:
            self.random_y2 = random.randint(200, 460)
            self.y2 = self.random_y2 - 1000

            if score > 38:
                self.y2 += 30
            elif score > 18:
                self.y2 += 15

            self.x2 = 450
            screen.blit(self.image1, (self.x2, self.random_y2))
            screen.blit(self.image2, (self.x2, self.y2))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('ground.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 685
        self.x = 0
        self.scrolling = 2

    def update(self):
        self.x -= self.scrolling

        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, 485))

        if self.x < 0:
            screen.blit(self.image, (self.x + 500, 485))


if __name__ == '__main__':
    start_screen()
    bird = Bird()
    pipes = Pipes()
    ground = Ground()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        if pygame.sprite.collide_mask(bird, ground):
            pygame.quit()
            sys.exit()

        bird.update()
        pipes.update()
        ground.update()

        image = load_image('background.jpg')
        background = pygame.transform.scale(image, SIZE)
        screen.blit(background, (0, 0))

        bird.draw(screen)
        pipes.draw(screen)
        ground.draw(screen)

        font = pygame.font.Font(None, 40)

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))

        pygame.display.update()

        clock.tick(FPS)
