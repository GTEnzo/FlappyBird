import datetime as dt
import pygame
import random
import sys
import csv
import os

FPS = 60  # кадры в секунду
SIZE = (WIDTH, HEIGHT) = (450, 600)  # размер окна
BIRD_SIZE = (45, 35)  # размер птички

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 116)
POINTED = (141, 199, 63)  # курсор наведён
NOT_POINTED = (255, 251, 214)  # курсор не наведён

score = 0  # очки
scrolling = 2  # скорость труб и земли
is_alive = True  # жива ли птичка
is_flying = False  # начата ли игра
random_number = random.randint(-750, -550)  # используется для рандомной генерации "y" труб

current_background = 'background1.jpg'  # ...фона
current_top_pipe = 'top_pipe1.png'  # ...верхней трубы
current_bottom_pipe = 'bottom_pipe1.png'  # ...нижней трубы
current_ground = 'ground1.png'  # ...земли

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

flap_sound = pygame.mixer.Sound(os.path.join('data', 'flap.wav'))
pipes_sound = pygame.mixer.Sound(os.path.join('data', 'pipes.wav'))
end_sound = pygame.mixer.Sound(os.path.join('data', 'end.wav'))


class Bird(pygame.sprite.Sprite):  # cпрайт птички
    def __init__(self):
        super().__init__(all_sprites)
        self.gravity = 0.6  # гравитация
        self.jump_strength = -9  # сила прыжка
        self.boost = 0  # вертикальная скорость

        # список изображений, которые используются для анимации птички в игре
        self.bird_shots = [pygame.transform.scale(load_image(f'bird{i}.png'), BIRD_SIZE) for i in range(1, 4)]

        self.shot = 0  # номер кадра
        self.image = self.bird_shots[self.shot]
        self.rect = self.image.get_rect()

        # изначальное положение птички
        self.rect.x = 150
        self.rect.y = 280

        self.mask = pygame.mask.from_surface(self.image)
        self.shots = 5
        self.num = 0

    def jump(self):  # прыжок птички
        global is_flying

        if not is_flying:  # если игра не была начата...
            is_flying = True  # ...она начата

        flap_sound.play()
        self.boost = self.jump_strength  # птичка прыгнула

    def update(self):  # обновление координат
        self.mask = pygame.mask.from_surface(self.image)

        if is_flying:  # если птичка прыгнула
            self.boost += self.gravity  # эффект гравитации
            self.rect.y += self.boost  # обновление вертикальной позиции птички

        self.num += 1
        if self.num >= self.shots:
            self.num = 0
            self.shot = (self.shot + 1) % len(self.bird_shots)  # текущий кадр
            self.image = self.bird_shots[self.shot]  # замена кадра

        if self.boost < 0:
            # вращение изображения птички в зависимости от её вертикальной скорости при взлёте
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], min(30, -self.boost * 4))
        elif self.boost > 0:
            # вращение изображения птички в зависимости от её вертикальной скорости при падении
            self.image = pygame.transform.rotate(self.bird_shots[self.shot], max(-70, self.boost * -8))
        else:
            self.image = self.bird_shots[self.shot]

    def draw(self, screen):  # рисование птички
        screen.blit(self.image, self.rect)


class TopPipe(pygame.sprite.Sprite):  # спрайт верхней трубы
    def __init__(self, x):
        global current_top_pipe
        super().__init__(all_sprites)
        self.image = load_image(current_top_pipe)
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
        global current_bottom_pipe
        super().__init__(all_sprites)
        self.image = load_image(current_bottom_pipe)
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
    def __init__(self, x):
        global current_ground
        super().__init__(all_sprites)
        self.image = load_image(current_ground)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = 485
        self.rect.x = x

    def update(self):  # обновление координат земли
        global scrolling

        self.rect.x -= scrolling  # движение земли

    def draw(self, screen):  # рисование земли
        screen.blit(self.image, (self.rect.x, self.rect.top))

        if self.rect.x < 0:  # если земля начала пропадать справа...
            screen.blit(self.image, (self.rect.x + WIDTH, self.rect.top))  # ...сшиваем две земли


def load_image(name, colorkey=None):  # обработка изображений
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):  # если не найдено
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
    global flap_sound, current_background, current_top_pipe, current_bottom_pipe, current_ground

    # Громкости звуков
    volume1 = flap_sound.get_volume()
    volume2 = pipes_sound.get_volume()
    volume3 = end_sound.get_volume()

    font = pygame.font.Font(None, 40)  # шрифт

    backgrounds = [  # изображения фонов
        'background1.jpg',
        'background2.jpg',
        'background3.jpg'
    ]

    top_pipes = [  # изображения верхней трубы
        'top_pipe1.png',
        'top_pipe2.png',
        'top_pipe3.png'
    ]

    bottom_pipes = [  # изображения нижней трубы
        'bottom_pipe1.png',
        'bottom_pipe2.png',
        'bottom_pipe3.png'
    ]

    grounds = [  # изображения земли
        'ground1.png',
        'ground2.png',
        'ground3.png'
    ]

    index = backgrounds.index(current_background)  # номер фона

    back_button = pygame.Surface((152, 50))  # кнопка "Back"
    back_text = font.render('Back', True, BLACK)
    back_text_rect = back_text.get_rect(
        center=(back_button.get_width() / 2,
                back_button.get_height() / 2))
    back_button_rect = pygame.Rect(5, 5, 152, 50)

    previous_button = pygame.Surface((50, 50))  # кнопка "<"
    previous_text = font.render('<', True, BLACK)
    previous_text_rect = previous_text.get_rect(
        center=(previous_button.get_width() / 2,
                previous_button.get_height() / 2))
    previous_button_rect = pygame.Rect(50, 350, 50, 50)

    next_button = pygame.Surface((50, 50))  # кнопка ">"
    next_text = font.render('>', True, BLACK)
    next_text_rect = next_text.get_rect(
        center=(next_button.get_width() / 2,
                next_button.get_height() / 2))
    next_button_rect = pygame.Rect(350, 350, 50, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если прожата...
                if back_button_rect.collidepoint(event.pos):  # ...кнопка "Back"...
                    running = False  # ...возврат в начальное окно

                if next_button_rect.collidepoint(event.pos):  # ...кнопка "<"...
                    # ...все изображения меняются на соответсвующие фону
                    index = (index + 1) % len(backgrounds)
                    current_background = backgrounds[index]
                    current_top_pipe = top_pipes[index]
                    current_bottom_pipe = bottom_pipes[index]
                    current_ground = grounds[index]

                if previous_button_rect.collidepoint(event.pos):  # ...кнопка ">"...
                    # ...все изображения меняются на соответсвующие фону
                    index = (index - 1) % len(backgrounds)
                    current_background = backgrounds[index]
                    current_top_pipe = top_pipes[index]
                    current_bottom_pipe = bottom_pipes[index]
                    current_ground = grounds[index]

            if event.type == pygame.KEYDOWN:  # если прожата...
                if event.key == pygame.K_LEFT:  # ...левая стрелка...
                    # ...громкость меньше
                    volume1 = max(0, volume1 - 0.1)
                    volume2 = max(0, volume2 - 0.1)
                    volume3 = max(0, volume3 - 0.1)

                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)

                if event.key == pygame.K_RIGHT:  # ...правая стрелка...
                    # ...громкость больше
                    volume1 = min(1, volume1 + 0.1)
                    volume2 = min(1, volume2 + 0.1)
                    volume3 = min(1, volume3 + 0.1)

                    flap_sound.set_volume(volume1)
                    pipes_sound.set_volume(volume2)
                    end_sound.set_volume(volume3)

        screen.fill(BLUE)

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(back_button, POINTED, (1, 1, 150, 48))
        else:
            pygame.draw.rect(back_button, NOT_POINTED, (1, 1, 150, 48))
        back_button.blit(back_text, back_text_rect)
        screen.blit(back_button, (back_button_rect.x, back_button_rect.y))

        if previous_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(previous_button, POINTED, (1, 1, 48, 48))
        else:
            pygame.draw.rect(previous_button, NOT_POINTED, (1, 1, 48, 48))
        previous_button.blit(previous_text, previous_text_rect)
        screen.blit(previous_button, (previous_button_rect.x, previous_button_rect.y))

        if next_button_rect.collidepoint(pygame.mouse.get_pos()):  # наведение курсора
            pygame.draw.rect(next_button, POINTED, (1, 1, 48, 48))
        else:
            pygame.draw.rect(next_button, NOT_POINTED, (1, 1, 48, 48))
        next_button.blit(next_text, next_text_rect)
        screen.blit(next_button, (next_button_rect.x, next_button_rect.y))

        image = pygame.transform.scale(load_image(backgrounds[index]), (200, 200))  # картинка текущего фона
        screen.blit(image, (125, 300))

        volume_text = font.render(f'Volume: {int(volume1 * 10)}', True, WHITE)  # текст громкости
        screen.blit(volume_text, (50, 210))

        instruction_text = font.render('Use LEFT/RIGHT', True, WHITE)
        instruction_text2 = font.render('arrows to adjust volume', True, WHITE)

        screen.blit(instruction_text, (50, 100))
        screen.blit(instruction_text2, (50, 135))

        pygame.display.update()

    start_screen()


def game_screen():  # игровое окно
    global score, is_alive, is_flying, random_number, current_background

    bird = Bird()  # вызов спрайта птички

    pipe1 = TopPipe(700)  # первая верхняя труба
    pipe2 = TopPipe(950)  # первая нижняя труба
    pipe3 = BottomPipe(700)  # вторая верхняя труба
    pipe4 = BottomPipe(950)  # вторая нижняя труба

    pipe1.get_random_number(random_number)  # присваевание "y"-а первой верхней трубе
    pipe3.get_random_number(random_number + 1000)  # присваевание "y"-а первой нижней трубе

    random_number = random.randint(-750, -550)  # получение нового значения

    pipe2.get_random_number(random_number)  # присваевание "y"-а второй верхней трубе
    pipe4.get_random_number(random_number + 1000)  # присваевание "y"-а второй нижней трубе

    pipes = pygame.sprite.Group()  # группа спрайтов труб
    pipes.add(pipe1, pipe2, pipe3, pipe4)  # добавление спрайтов в группу

    ground = Ground(0)  # вызов спрайта земли

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

            # усложнение в зависимости от пройденного расстояния
            if score > 38:
                pipe1.get_random_number(random_number)
                pipe3.get_random_number(random_number + 940)
            elif score > 18:
                pipe1.get_random_number(random_number)
                pipe3.get_random_number(random_number + 950)
            elif score > 8:
                pipe1.get_random_number(random_number)
                pipe3.get_random_number(random_number + 960)
            elif score > 3:
                pipe1.get_random_number(random_number)
                pipe3.get_random_number(random_number + 980)
            else:
                pipe1.get_random_number(random_number)
                pipe3.get_random_number(random_number + 1000)

            pipes.add(pipe1, pipe3)

        if pipe2.rect.right <= 0:
            pipe2 = TopPipe(450)
            pipe4 = BottomPipe(450)

            random_number = random.randint(-750, -550)

            # усложнение в зависимости от пройденного расстояния
            if score > 38:
                pipe2.get_random_number(random_number)
                pipe4.get_random_number(random_number + 940)
            elif score > 18:
                pipe2.get_random_number(random_number)
                pipe4.get_random_number(random_number + 950)
            elif score > 8:
                pipe2.get_random_number(random_number)
                pipe4.get_random_number(random_number + 960)
            elif score > 3:
                pipe2.get_random_number(random_number)
                pipe4.get_random_number(random_number + 980)
            else:
                pipe2.get_random_number(random_number)
                pipe4.get_random_number(random_number + 1000)

            pipes.add(pipe2, pipe4)

        if ground.rect.x < -WIDTH:
            ground = Ground(0)

        if pygame.sprite.collide_mask(bird, ground) or pygame.sprite.spritecollide(bird, pipes,
                                                                                   False) or bird.rect.y < -200:  # если произошло столкновение

            with open('records.csv', 'a', newline='', encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow([dt.datetime.now().date(), score])  # запись очков в таблицу

            end_sound.play()
            end_screen(score)  # вызов конечного окна

        else:
            bird.update()
            if is_flying:
                pipes.update()
            ground.update()

        image = pygame.transform.scale(load_image(current_background), SIZE)  # фон
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


def end_screen(s):  # конец игры
    global score, is_alive, is_flying

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:  # если прожата "M"
                is_flying = False
                start_screen()  # выход в меню
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                    event.type == pygame.MOUSEBUTTONDOWN):  # если прожата мышка или пробел
                is_flying = False
                game_screen()  # рестарт

        font = pygame.font.Font(None, 30)  # шрифт

        text1 = font.render(f'Game over!', True, WHITE)
        text2 = font.render(f'You scored {s} points', True, WHITE)
        text3 = font.render(f'Click SPACE to restart', True, WHITE)
        text4 = font.render(f'Click M or left button to move in menu', True, WHITE)

        screen.blit(text1, (50, 100))
        screen.blit(text2, (50, 150))
        screen.blit(text3, (50, 250))
        screen.blit(text4, (50, 300))

        score = 0

        pygame.display.update()

        clock.tick(FPS)


start_screen()  # запуск меню
