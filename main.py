import datetime as dt
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
BLUE = (0, 122, 116)

score = 0
is_alive = True
is_flying = False

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.bird_x = 150
        self.bird_y = 280
        self.gravity = 0.6
        self.jump_strength = -9
        self.boost = 0
        self.bird_shots = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]
        self.shot = 0
        self.bird = self.bird_shots[self.shot]
        self.rect = self.bird.get_rect(topleft=(self.bird_x, self.bird_y))
        self.mask = pygame.mask.from_surface(self.bird)
        self.shots = 5
        self.num = 0

    def jump(self):
        global is_flying

        if not is_flying:
            is_flying = True
        self.boost = self.jump_strength

    def update(self):
        if is_flying:
            self.boost += self.gravity
            self.bird_y += self.boost

            if self.bird_y > HEIGHT - 150:
                self.bird_y = HEIGHT - 150
                self.boost = 0

        self.rect.y = self.bird_y
        self.num += 1
        if self.num >= self.shots:
            self.num = 0
            self.shot = (self.shot + 1) % len(self.bird_shots)
            self.bird = self.bird_shots[self.shot]

        if self.boost < 0:
            self.bird = pygame.transform.rotate(self.bird_shots[self.shot], min(25, max(0, -self.boost * 4)))
        elif self.boost > 0:
            self.bird = pygame.transform.rotate(self.bird_shots[self.shot], max(-70, min(0, self.boost * -8)))
        else:
            self.bird = self.bird_shots[self.shot]

        self.rect = self.bird.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.bird, self.rect)


class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.pipe_b = load_image('pipe1.png')
        self.pipe_t = load_image('pipe2.png')
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

        screen.blit(self.pipe_b, (self.x1, self.random_y1))
        screen.blit(self.pipe_t, (self.x1, self.y1))
        screen.blit(self.pipe_b, (self.x2, self.random_y2))
        screen.blit(self.pipe_t, (self.x2, self.y2))

        if self.x1 < -50:
            self.random_y1 = random.randint(200, 460)
            self.y1 = self.random_y1 - 1000

            if score > 38:
                self.y1 += 30
            elif score > 18:
                self.y1 += 15

            self.x1 = 450
            screen.blit(self.pipe_b, (self.x1, self.random_y1))
            screen.blit(self.pipe_t, (self.x1, self.y1))

        if self.x2 < -50:
            self.random_y2 = random.randint(200, 460)
            self.y2 = self.random_y2 - 1000

            if score > 38:
                self.y2 += 30
            elif score > 18:
                self.y2 += 15

            self.x2 = 450
            screen.blit(self.pipe_b, (self.x2, self.random_y2))
            screen.blit(self.pipe_t, (self.x2, self.y2))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.ground = load_image('ground.png')
        self.rect = self.ground.get_rect()
        self.mask = pygame.mask.from_surface(self.ground)
        self.rect.bottom = 685
        self.x = 0
        self.scrolling = 2

    def update(self):
        self.x -= self.scrolling

        if self.x <= -WIDTH:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.ground, (self.x, 485))

        if self.x < 0:
            screen.blit(self.ground, (self.x + 500, 485))


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
    global is_alive

    is_alive = True

    screen.fill(BLUE)

    logo = pygame.transform.scale(load_image('logo.png'), (360, 90))
    screen.blit(logo, (45, 45))

    font = pygame.font.Font(None, 60)

    start_button = pygame.Surface((300, 75))
    start_text = font.render('Start', True, BLACK)
    start_rect = start_text.get_rect(
        center=(start_button.get_width() / 2,
                start_button.get_height() / 2))
    start_button_rect = pygame.Rect(75, 220, 300, 75)

    leaders_button = pygame.Surface((300, 75))
    leaders_text = font.render('Records', True, BLACK)
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
                    game_screen()
                if leaders_button_rect.collidepoint(event.pos):
                    records_window()

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


def records_window():
    window = pygame.display.set_mode(SIZE)
    window.fill(BLUE)

    with open('records.csv', encoding="utf8") as csvfile:
        file = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        records = sorted(file, key=lambda x: int(x['points']), reverse=True)

    font = pygame.font.Font(None, 40)

    y = 100
    place = 1
    for i in records:
        name = font.render(f'{place}. {i["name"]}:', True, WHITE)
        screen.blit(name, (50, y))

        points = font.render(f'{i["points"]}', True, WHITE)
        screen.blit(points, (350, y))

        y += 40
        if place < 10:
            place += 1
        else:
            break

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


def game_screen():
    global score, is_alive, is_flying

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                is_alive = False
                is_flying = False
                score = 0
                start_screen()

        if pygame.sprite.collide_mask(bird, ground):
            with open('records.csv', 'a', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow([dt.datetime.now().date(), score])

            score = 0
            end_screen()

        else:
            bird.update()
            if is_flying:
                pipes.update()
            ground.update()

        background = pygame.transform.scale(load_image('background.jpg'), SIZE)
        screen.blit(background, (0, 0))

        bird.draw(screen)
        pipes.draw(screen)
        ground.draw(screen)

        font = pygame.font.Font(None, 40)

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))

        pygame.display.update()

        clock.tick(FPS)


def end_screen():
    global score, is_alive, is_flying

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_flying = False
                game_screen()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                is_flying = False
                score = 0
                start_screen()

        font = pygame.font.Font(None, 30)

        text1 = font.render(f'Game over!', True, WHITE)
        text2 = font.render(f'Click SPACE to restart.', True, WHITE)
        text3 = font.render(f'Click M to move in menu', True, WHITE)

        screen.blit(text1, (100, 100))
        screen.blit(text2, (100, 200))
        screen.blit(text3, (100, 250))

        pygame.display.update()

        clock.tick(FPS)


start_screen()
