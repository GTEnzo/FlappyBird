from pygame import mixer
import datetime as dt
import pygame
import random
import sys
import csv
import os

'''Константы'''
FPS = 60  # кадры в секунду
SIZE = (WIDTH, HEIGHT) = (450, 600)  # размер окна
BIRD_SIZE = (45, 35)  # размер птички

'''Используемые цвета'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 116)
POINTED = (141, 199, 63)  # курсор наведён на кнопку
NOT_POINTED = (255, 251, 214)  # курсор не наведён на кнопку

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

'''Звуки'''
flap_sound = mixer.Sound(os.path.join('data', 'flap.wav'))
pipes_sound = mixer.Sound(os.path.join('data', 'pipes.wav'))
end_sound = mixer.Sound(os.path.join('data', 'end.wav'))


class Bird(pygame.sprite.Sprite):  # спрайт птички
    def __init__(self):
        super().__init__(all_sprites)
        self.gravity = 0.6
        self.jump_strength = -9  # Сила прыжка
        self.boost = 0  # Вертикальная скорость

        # Cписок изображений, которые используются для анимации птички в игре
        self.bird_shots = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]

        self.shot = 0  # Кадр
        self.image = self.bird_shots[self.shot]  # Хранение текущего изображения
        self.rect = self.image.get_rect()  # Прямоугольник для текущего изображения птички
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
        self.boost = self.jump_strength  # Птичка прыгнула

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)  # Создание маски

        if is_flying:  # Если птичка прыгнула
            self.boost += self.gravity  # Эффект гравитации
            self.rect.y += self.boost  # Обновление вертикальной позиции птички

            if self.rect.y > HEIGHT - 150:  # Проверка на выход птички за пределы экрана
                self.rect.y = HEIGHT - 150
                self.boost = 0

        self.num += 1
        if self.num >= self.shots:
            self.num = 0
            self.shot = (self.shot + 1) % len(self.bird_shots)  # Текущий кадр
            self.image = self.bird_shots[self.shot]  # Замена кадра

        if self.boost < 0:
            # Вращение изображения птички в зависимости от её вертикальной скорости при взлёте
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], min(30, -self.boost * 4))
        elif self.boost > 0:
            # Вращение изображения птички в зависимости от её вертикальной скорости при падении
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], max(-70, self.boost * -8))
        else:
            self.image = self.bird_shots[self.shot]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TopPipe(pygame.sprite.Sprite):  # спрайт верхней трубы
    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = load_image('top_pipe.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

    def get_random_number(self, r):  # импорт рандомного значения
        self.rect.y = r  # присваевание "y"-у трубы рандомное значение

    def update(self):  # обновление координат труб и начисление очков
        global score, scrolling

        self.rect.x -= scrolling  # движение трубы

        if self.rect.x == 150:  # если птичка пролетела трубу...
            score += 1  # ...+1 очко
            pipes_sound.play()

        if self.rect.right < 0:  # если труба не в пределах экрана...
            self.kill()  # ...она удаляется

    def draw(self, screen):  # рисование труб
        if self.rect.x < -50:  # если труба пропала...
            self.rect.x = 450  # ...она перемещается обратно

        screen.blit(self.image, (self.rect.x, self.rect.y))


class BottomPipe(pygame.sprite.Sprite):  # спрайт нижней трубы
    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = load_image('bottom_pipe.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.mask = pygame.mask.from_surface(self.image)

    def get_random_number(self, r):  # импорт рандомного значения
        self.rect.y = r  # присваевание "y"-у трубы рандомное значение

    def update(self):  # обновление координат труб
        global scrolling

        self.rect.x -= scrolling  # движение трубы

        if self.rect.right < 0:  # если труба не в пределах экрана...
            self.kill()  # ...она удаляется

    def draw(self, screen):  # рисование труб
        if self.rect.x < -50:  # если труба пропала...
            self.rect.x = 450  # ...она перемещается обратно

        screen.blit(self.image, (self.rect.x, self.rect.y + 1000))


class Ground(pygame.sprite.Sprite):  # спрайт земли
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('ground.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = 700
        self.rect.x = 0

    def update(self):  # обновление координат земли
        global scrolling

        self.rect.x -= scrolling  # движение земли

        if self.rect.right <= 0:  # если земля полностью исчезла...
            self.rect.x = 0  # ...она возвращается в пределы окна

    def draw(self, screen):  # рисование земли
        screen.blit(self.image, (self.rect.x, 485))

        if self.rect.x < 0:  # если земля начала пропадать справа...
            screen.blit(self.image, (self.rect.x + 500, 485))  # ...сшиваем две земли


def load_image(name, colorkey=None):  # импорт картинок
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


def start_screen():  # начальное окно
    global is_alive

    is_alive = True  # птица жива

    screen.fill(BLUE)

    image = pygame.transform.scale(load_image('logo.png'), (360, 90))  # логотип
    screen.blit(image, (45, 45))

    font = pygame.font.Font(None, 60)  # шрифт

    start_button = pygame.Surface((300, 75))  # кнопка "Start"
    start_text = font.render('Start', True, BLACK)
    start_text_rect = start_text.get_rect(
        center=(start_button.get_width() / 2,
                start_button.get_height() / 2))
    start_button_rect = pygame.Rect(75, 220, 300, 75)

    records_button = pygame.Surface((300, 75))  # кнопка "Records"
    records_text = font.render('Records', True, BLACK)
    records_text_rect = records_text.get_rect(
        center=(records_button.get_width() / 2,
                records_button.get_height() / 2))
    records_button_rect = pygame.Rect(75, 320, 300, 75)

    settings_button = pygame.Surface((300, 75))  # кнопка "Settings"
    settings_text = font.render('Settings', True, BLACK)
    settings_text_rect = settings_text.get_rect(
        center=(settings_button.get_width() / 2,
                settings_button.get_height() / 2))
    settings_button_rect = pygame.Rect(75, 420, 300, 75)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если прожата...
                if start_button_rect.collidepoint(event.pos):  # ...кнопка "Start"...
                    game_screen()  # ...запускается игра
                if records_button_rect.collidepoint(event.pos):  # ...кнопка "Records"...
                    records_window()  # ...открывается окно рекордов
                if settings_button_rect.collidepoint(event.pos):  # ...кнопка "Settings"...
                    settings_window()  # ...открывается окно настроек

        if start_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(start_button, POINTED, (1, 1, 298, 73))
        else:
            pygame.draw.rect(start_button, NOT_POINTED, (1, 1, 298, 73))
        start_button.blit(start_text, start_text_rect)
        screen.blit(start_button, (start_button_rect.x, start_button_rect.y))

        if records_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(records_button, POINTED, (1, 1, 298, 73))
        else:
            pygame.draw.rect(records_button, NOT_POINTED, (1, 1, 298, 73))
        records_button.blit(records_text, records_text_rect)
        screen.blit(records_button, (records_button_rect.x, records_button_rect.y))

        if settings_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(settings_button, POINTED, (1, 1, 298, 73))
        else:
            pygame.draw.rect(settings_button, NOT_POINTED, (1, 1, 298, 73))
        settings_button.blit(settings_text, settings_text_rect)
        screen.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))

        pygame.display.update()


def records_window():  # окно рекордов
    window = pygame.display.set_mode(SIZE)
    window.fill(BLUE)

    with open('records.csv', encoding="utf8") as csvfile:  # открытие таблицы
        file = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        records = sorted(file, key=lambda x: int(x['points']), reverse=True)  # создание списка

    font = pygame.font.Font(None, 40)  # шрифт

    y = 100
    place = 1
    for i in records:  # упорядоченное распределение первых 10 рекордов
        name = font.render(f'{place}. {i["name"]}:', True, WHITE)
        screen.blit(name, (50, y))
        points = font.render(f'{i["points"]}', True, WHITE)
        screen.blit(points, (350, y))

        y += 40
        if place < 10:
            place += 1
        else:
            break

    back_button = pygame.Surface((152, 50))  # кнопка "Back"
    back_text = font.render('Back', True, BLACK)
    back_text_rect = back_text.get_rect(
        center=(back_button.get_width() / 2,
                back_button.get_height() / 2))
    back_button_rect = pygame.Rect(5, 5, 152, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если прожата...
                if back_button_rect.collidepoint(event.pos):  # ...кнопка "Back"...
                    running = False  # ...возврат в начальное окно

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(back_button, POINTED, (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, NOT_POINTED, (1, 1, 150, 48))
        back_button.blit(back_text, back_text_rect)
        window.blit(back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.update()

    start_screen()


def settings_window():  # окно настроек
    global flap_sound

    volume1 = flap_sound.get_volume()
    volume2 = pipes_sound.get_volume()
    volume3 = end_sound.get_volume()

    font = pygame.font.Font(None, 40)

    back_button = pygame.Surface((152, 50))
    back_text = font.render('Back', True, BLACK)
    back_text_rect = back_text.get_rect(
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    volume1 = max(0, volume1 - 0.05)
                    volume2 = max(0, volume2 - 0.05)
                    volume3 = max(0, volume3 - 0.05)
                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)
                if event.key == pygame.K_RIGHT:
                    volume1 = min(1, volume1 + 0.05)
                    volume2 = min(1, volume2 + 0.05)
                    volume3 = min(1, volume3 + 0.05)
                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)

        screen.fill(BLUE)

        volume_text = font.render(f'Volume: {int(volume1 * 20)}', True, WHITE)
        screen.blit(volume_text, (50, 240))

        instruction_text1 = font.render('Use LEFT/RIGHT', True, WHITE)
        instruction_text2 = font.render('arrows to adjust volume', True, WHITE)

        screen.blit(instruction_text1, (50, 120))
        screen.blit(instruction_text2, (50, 160))

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(back_button, POINTED, (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, NOT_POINTED, (1, 1, 150, 48))
        back_button.blit(back_text, back_text_rect)
        screen.blit(back_button, (back_button_rect.x, back_button_rect.y))

        pygame.display.update()

    start_screen()


def game_screen():  # игровое окно
    global score, is_alive, is_flying, random_number

    bird = Bird()  # вызов класса птички

    pipe1 = TopPipe(700)  # верхняя труба 1
    pipe2 = TopPipe(950)  # верхняя труба 2
    pipe3 = BottomPipe(700)  # нижняя труба 1
    pipe4 = BottomPipe(950)  # нижняя труба 2

    # Получение рандомных значений
    pipe1.get_random_number(random_number)
    pipe3.get_random_number(random_number + 1000)

    random_number = random.randint(-750, -550)

    pipe2.get_random_number(random_number)
    pipe4.get_random_number(random_number + 1000)

    pipes = pygame.sprite.Group()
    pipes.add(pipe1, pipe2, pipe3, pipe4)

    ground = Ground()  # вызов класса земли

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):  # если прожата мышка или пробел
                bird.jump()  # птичка прыгает
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # если прожата "M"
                score = 0
                is_alive = False
                is_flying = False
                start_screen()  # выход в меню

        if pipe1.rect.right <= 0:
            pipe1 = TopPipe(450)
            pipe3 = BottomPipe(450)

            random_number = random.randint(-750, -550)

            pipe1.get_random_number(random_number)
            pipe3.get_random_number(random_number + 1000)

            pipes.add(pipe1, pipe3)

        if pipe2.rect.right <= 0:
            pipe2 = TopPipe(450)
            pipe4 = BottomPipe(450)

            random_number = random.randint(-750, -550)

            pipe2.get_random_number(random_number)
            pipe4.get_random_number(random_number + 1000)

            pipes.add(pipe2, pipe4)

        if pygame.sprite.collide_mask(bird, ground) or pygame.sprite.spritecollide(bird, pipes,
                                                                                   False) or bird.rect.y < -200:  # если произошло столкновение

            with open('records.csv', 'a', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow([dt.datetime.now().date(), score])  # запись очков в таблицу

            score = 0
            end_sound.play()
            end_screen()  # вызов конечного окна

        else:
            bird.update()
            if is_flying:
                pipes.update()
            ground.update()

        image = pygame.transform.scale(load_image('background.jpg'), SIZE)  # фон
        screen.blit(image, (0, 0))

        bird.draw(screen)
        if is_alive:
            pipes.draw(screen)
        ground.draw(screen)

        font = pygame.font.Font(None, 40)  # шрифт

        text = font.render(f'Score: {score}', True, WHITE)  # текст очков
        screen.blit(text, (20, 20))

        pygame.display.update()

        clock.tick(FPS)


def end_screen():  # конец игры
    global score, is_alive, is_flying

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # если прожата "M"
                score = 0
                is_flying = False
                start_screen()  # выход в меню
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                    event.type == pygame.MOUSEBUTTONDOWN):  # если прожата мышка или пробел
                is_flying = False
                game_screen()  # рестарт

        font = pygame.font.Font(None, 30)  # шрифт

        text1 = font.render(f'Game over!', True, WHITE)
        text2 = font.render(f'Click SPACE to restart', True, WHITE)
        text3 = font.render(f'Click M or left button to move in menu', True, WHITE)

        screen.blit(text1, (50, 100))
        screen.blit(text2, (50, 200))
        screen.blit(text3, (50, 250))

        pygame.display.update()

        clock.tick(FPS)


start_screen()
