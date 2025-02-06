import datetime as dt
import pygame
from pygame import mixer
import random
import sys
import csv
import os

'''Константы'''
FPS = 60  # кадры в секунду
SIZE = (WIDTH, HEIGHT) = (450, 600)  # размер окна
BIRD_SIZE = (45, 35)  # размер птички
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 116)

'''Глобальные переменные'''
score = 0  # очки
scrolling = 2  # скорость труб и земли
is_alive = True  # жива ли птичка
is_flying = False  # начата ли игра
random_number = random.randint(-750, -550)  # используется для рандомной генерации "y" труб

'''Вызов pygame'''
pygame.init()
mixer.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
flap_sound = mixer.Sound(os.path.join('data', 'flap.wav'))
pipes_sound = mixer.Sound(os.path.join('data', 'pipes.wav'))
end_sound = mixer.Sound(os.path.join('data', 'end.wav'))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.gravity = 0.6
        self.jump_strength = -9
        self.boost = 0
        self.bird_shots = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]
        self.shot = 0
        self.image = self.bird_shots[self.shot]
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 280
        self.mask = pygame.mask.from_surface(self.image)
        self.shots = 5
        self.num = 0

    def jump(self):
        global is_flying

        if not is_flying:
            is_flying = True

        flap_sound.play()
        self.boost = self.jump_strength

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)

        if is_flying:
            self.boost += self.gravity
            self.rect.y += self.boost

            if self.rect.y > HEIGHT - 150:
                self.rect.y = HEIGHT - 150
                self.boost = 0

        self.num += 1
        if self.num >= self.shots:
            self.num = 0
            self.shot = (self.shot + 1) % len(self.bird_shots)
            self.image = self.bird_shots[self.shot]

        if self.boost < 0:
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], min(25, max(0, -self.boost * 4)))
        elif self.boost > 0:
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], max(-70, min(0, self.boost * -8)))
        else:
            self.image = self.bird_shots[self.shot]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = load_image('top_pipe.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

    def get_num(self, r):
        self.rect.y = r

    def update(self):
        global score, scrolling

        self.rect.x -= scrolling

        if self.rect.x == 150:
            score += 1
            pipes_sound.play()

        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        if self.rect.x < -50:
            self.rect.x = 450

        self.rect.y = random.randint(-750, -550)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = load_image('bottom_pipe.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

    def get_num(self, r):
        self.rect.y = r

    def update(self):
        global scrolling

        self.rect.x -= scrolling

        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        if self.rect.x < -50:
            self.rect.x = 450

        self.rect.y = random.randint(-750, -550)
        screen.blit(self.image, (self.rect.x, self.rect.y + 1000))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('ground.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 700
        self.rect.x = 0

    def update(self):
        global scrolling

        self.rect.x -= scrolling

        if self.rect.x <= -WIDTH:
            self.rect.x = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, 485))

        if self.rect.x < 0:
            screen.blit(self.image, (self.rect.x + 500, 485))


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

    image = pygame.transform.scale(load_image('logo.png'), (360, 90))
    screen.blit(image, (45, 45))

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

    settings_button = pygame.Surface((300, 75))
    settings_text = font.render('Settings', True, BLACK)
    settings_rect = settings_text.get_rect(
        center=(settings_button.get_width() / 2,
                settings_button.get_height() / 2))
    settings_button_rect = pygame.Rect(75, 420, 300, 75)

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
                if settings_button_rect.collidepoint(event.pos):
                    settings_window()

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

        if settings_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(settings_button, (141, 199, 63), (1, 1, 298, 73))
        else:
            pygame.draw.rect(settings_button, (255, 251, 214), (1, 1, 298, 73))
        settings_button.blit(settings_text, settings_rect)
        screen.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))

        pygame.display.update()


def settings_window():
    global flap_sound

    running = True
    volume1 = flap_sound.get_volume()
    volume2 = pipes_sound.get_volume()
    volume3 = end_sound.get_volume()

    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    volume1 = max(0, volume1 - 0.05)
                    volume2 = max(0, volume2 - 0.05)
                    volume3 = max(0, volume3 - 0.05)
                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)

                if event.key == pygame.K_RIGHT:
                    volume1 = max(0, volume1 + 0.05)
                    volume2 = max(0, volume2 + 0.05)
                    volume3 = max(0, volume3 + 0.05)
                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)

        screen.fill(BLUE)

        volume_text = font.render(f'Volume: {int(volume1 * 100)}%', True, WHITE)
        screen.blit(volume_text, (50, 200))

        instruction_text = small_font.render('Use LEFT/RIGHT', True, WHITE)
        instruction_text2 = small_font.render('arrows to adjust volume', True, WHITE)
        screen.blit(instruction_text, (50, 120))
        screen.blit(instruction_text2, (50, 150))

        back_button = pygame.Surface((152, 50))
        back_text = font.render('Back', True, BLACK)
        back_rect = back_text.get_rect(
            center=(back_button.get_width() / 2,
                    back_button.get_height() / 2))
        back_button_rect = pygame.Rect(5, 5, 152, 50)

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(back_button, (141, 199, 63), (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, (255, 251, 214), (1, 1, 150, 48))
        back_button.blit(back_text, back_rect)
        screen.blit(back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.update()

    start_screen()


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
        name = font.render(f'{place}. {i['name']}:', True, WHITE)
        screen.blit(name, (50, y))
        points = font.render(f'{i['points']}', True, WHITE)
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
    global score, is_alive, is_flying, random_number

    bird = Bird()

    pipe1 = TopPipe(700)
    pipe2 = TopPipe(950)
    pipe3 = BottomPipe(700)
    pipe4 = BottomPipe(950)

    pipe1.get_num(random_number)
    pipe3.get_num(random_number + 1000)

    random_number = random.randint(-750, -550)

    pipe2.get_num(random_number)
    pipe4.get_num(random_number + 1000)

    pipes = pygame.sprite.Group()
    pipes.add(pipe1, pipe2, pipe3, pipe4)

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
                score = 0
                is_alive = False
                is_flying = False
                start_screen()

        if pipe1.rect.x <= -50:
            pipe1 = TopPipe(450)
            pipe3 = BottomPipe(450)

            random_number = random.randint(-750, -550)

            pipe1.get_num(random_number)
            pipe3.get_num(random_number + 1000)

            pipes.add(pipe1, pipe3)

        if pipe2.rect.x <= -50:
            pipe2 = TopPipe(450)
            pipe4 = BottomPipe(450)

            random_number = random.randint(-750, -550)

            pipe2.get_num(random_number)
            pipe4.get_num(random_number + 1000)

            pipes.add(pipe2, pipe4)

        if pygame.sprite.collide_mask(bird, ground) or pygame.sprite.spritecollide(bird, pipes,
                                                                                   False) or bird.rect.y < -200:

            with open('records.csv', 'a', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow([dt.datetime.now().date(), score])

            score = 0
            end_sound.play()
            end_screen()

        else:
            bird.update()
            if is_flying:
                pipes.update()
            ground.update()

        image = pygame.transform.scale(load_image('background.jpg'), SIZE)
        screen.blit(image, (0, 0))

        bird.draw(screen)
        if is_alive:
            pipes.draw(screen)
        ground.draw(screen)

        font = pygame.font.Font(None, 40)

        text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(text, (20, 20))

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                score = 0
                is_flying = False
                start_screen()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                is_flying = False
                game_screen()

        font = pygame.font.Font(None, 30)

        text1 = font.render(f'Game over!', True, WHITE)
        text2 = font.render(f'Click SPACE to restart.', True, WHITE)
        text3 = font.render(f'Click M or left button to move in menu', True, WHITE)

        screen.blit(text1, (50, 100))
        screen.blit(text2, (50, 200))
        screen.blit(text3, (50, 250))

        pygame.display.update()

        clock.tick(FPS)


start_screen()
