import random #імпорт функції вибору випадкової події
import os

import pygame #імпорт бібліотеки
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT #імпорт константи "вихід", "клавіша вниз", "кл.вгору", "кл.ліворуч", "кл.праворуч"

pygame.init() #ініціювання бібліотеки

FPS = pygame.time.Clock() #константа, для задання швидкості зміни координат ("тіків")

HEIGHT = 800 #висота вікна гри
WIDTH = 1200 #ширина вікна гри

FONT = pygame.font.SysFont('Verdana', 50) #шрифт та розмір тексту, що відображуватиме бонуси

COLOR_WHITE = (255, 255, 255) #константа, що задає білий колір
COLOR_BLACK = (0, 0, 0) #константа, що задає чорний колір
COLOR_RED = (255, 0, 0) #константа, що задає червоний колір
COLOR_BLUE = (0, 0, 255) #константа, що задає синій колір

main_display = pygame.display.set_mode((WIDTH, HEIGHT)) #назначення змінної, котра зберігає вікно гри + вказуємо розміри вікна

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT)) #завантаження картинки з трансформуванням під певний розмір
bg_X1 = 0 #координата розміщення 1-ї картинки
bg_X2 = bg.get_width() #координата розміщення 2-ї картинки
bg_move = 3 #швідкість руху фонового зображення

IMAGE_PATH = "Goose" #змінна, котра описує шлях до картинок
PLAYER_IMAGES = os.listdir(IMAGE_PATH) #зчитуємо всі картинки з папки в одну константу
print(PLAYER_IMAGES)

player_size = (20, 20) #константа, що задає розмір "персонажа"
player = pygame.image.load('player.png').convert_alpha() # pygame.Surface(player_size) #створення певного "персонажа" з (розміром)
# player.fill(COLOR_BLACK) #заповнення кольором / задання кольору "персонажу"
player_rect = player.get_rect(topleft=(200, 300)) #задає початкові координати (для верхнього лівого кута прямокутника яким окреслено об'єкт)
player_move_down = [0, 4] #рух вниз
player_move_up = [0,-4] #рух вгору
player_move_right = [4, 0] #рух праворуч
player_move_left = [-4, 0] #рух ліворуч


def create_enemy(): #функція
    enemy_size = (30, 30) #константа, що задає розмір "ворога"
    enemy = pygame.image.load('enemy.png').convert_alpha() # pygame.Surface(enemy_size) # створення "ворога"
    # enemy.fill(COLOR_RED) #задаємо колір "ворога"
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-100), *enemy_size) #задає початкові координати "ворога"
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move] #вказуємо, що саме буде повертати функція

CREATE_ENEMY = pygame.USEREVENT + 1 #оголошуємо константу
pygame.time.set_timer(CREATE_ENEMY, 1500) #інтервал створення об'єкта

enemies = []

def create_bonus():
    bonus_size = (40, 40)
    bonus = pygame.image.load('bonus.png').convert_alpha() # pygame.Surface(bonus_size)
    # bonus.fill(COLOR_BLUE)
    bonus_rect = pygame.Rect(random.randint(200, WIDTH-200), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

bonuses = []

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

score = 0

image_index = 0

playing = True #змінна циклу гри

while playing: #початок циклу
    FPS.tick(240) #кількість "тіків" в мілісекунду

    for event in pygame.event.get(): #цикл продовжується поки playing=істина
        if event.type == QUIT: #коли спрацьовує "вихід"
            playing = False #змінній присвоюється значення "помилка" й цикл припиняється (вікно гри закривається)
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        
    # main_display.fill(COLOR_BLACK) #зафарбовування сліду від переміщення "персонажу"
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0)) #вставка фонового зображення
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed() 

    if keys[K_DOWN] and player_rect.bottom < HEIGHT: #якщо натиснута клавіша "вниз" і не вийшли за нижню межу вікна - рухаємось вниз
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0: #якщо натиснута клавіша "вгору" і не вийшли за верхню межу вікна - рухаємось вгору
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH: #якщо натиснута клавіша "праворуч" і не вийшли за праву межу вікна - рухаємось праворуч
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0: #якщо натиснута клавіша "ліворуч" і не вийшли за ліву межу вікна - рухаємось ліворуч
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
        if player_rect.colliderect(enemy[1]): #при зіткненні "персонажа" з "ворогом" гра завершується
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]): 
            score += 1 #при зіткненні нараховуємо 1 бонус
            bonuses.pop(bonuses.index(bonus)) #при зіткненні "персонажа" з "бонусом" бонус зникає з екрану

    main_display.blit(FONT.render(str (score), True, COLOR_BLUE), (WIDTH-50, 20)) #відображення набраних бонусів певним кольором, в певному місці
    main_display.blit(player, player_rect) #розміщення об'єкту на ігровому полі в певних координатах

    pygame.display.flip() #метод, що оновлює дисплей

    for enemy in enemies: #видалення "ворога", що досягнув лівого краю вікна
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))