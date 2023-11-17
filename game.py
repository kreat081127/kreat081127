import pygame as pg
import random
from os import path
from sql_bd import DateBaseSQL
db = DateBaseSQL()

img_dir = path.join(path.dirname(__file__), 'img') #изображает изображение в базе данных

WIDTH, HEIGHT = 480, 600 # отвечает за ширину предмета (элемента)
FPS = 50
r = [15,115,210,307,407] # кординаты

FONT_SIZE = 18
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (50,50,50)
pg.init() # расширяет блоки
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Project by Никита")
clock = pg.time.Clock() # поддержка ссортировки

font_name = pg.font.match_font('arial')
heart = pg.image.load(path.join(img_dir, "heart.png")).convert()
player_img = pg.image.load(path.join(img_dir, "Player_car.png")).convert()
car_png = []
car_list = ["G_car.png", "W_car.png","Gr_car.png"]

for img in car_list:
    car_png.append(pg.image.load(path.join(img_dir, img)).convert())

     
def draw_text(surf, text, x, y, size=FONT_SIZE, color=WHITE): # отображение текста
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color) 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect) 


def user_name(surf, text, x, y, size=FONT_SIZE): 
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect() 
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pg.sprite.Sprite): # daet Bosmoжность что-то делать в объекте
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (120, 150))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 
        self.rect.bottom = HEIGHT - 10 

    def update(self): # не нашел
        self.speedx = 0 
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]: 
            self.speedx = -8
        if keystate[pg.K_RIGHT]: 
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH + 31:
            self.rect.right = WIDTH + 31
        if self.rect.left < -31:
            self.rect.left = -31
        if keystate[pg.K_UP]:
            self.speedy = -8
        if keystate[pg.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy
        if self.rect.top < -10 :
            self.rect.top = -10
        if self.rect.bottom > HEIGHT + 13:
            self.rect.bottom = HEIGHT + 13
class Mob(pg.sprite.Sprite): # не нашел
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(car_png)
        self.image_orig = pg.transform.scale(self.image_orig, (70,120))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig 
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(r)
        self.rect.y = random.randrange(-150, -100) 
        self.speedy = 10

    def update(self):
        self.rect.y += 10
       
class Heart(pg.sprite.Sprite):
    def __init__(self, x, y): # оболчка базы данных
        pg.sprite.Sprite.__init__(self) # процес инцилизации этого класса
        self.image = pg.transform.scale(heart, (40, 40)) # размер изображения
        self.image.set_colorkey(BLACK) # удаление черного цвета
        self.rect = self.image.get_rect() # определение позиционирования объекта
        self.rect.x = x # кординаты по иксу
        self.rect.y = y # кординаты по игрику

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group() # разделяет память и локи
hearts = [] # список
player = Player() # экземпляр класса
all_sprites.add(player) # список в который добавляется
for i in range(3): # колл-во изображения
    h = Heart(i * 50, HEIGHT - 600)
    all_sprites.add(h)
    hearts.append(h)

def update_game_screen(name: str, score: int):
    screen.fill(DARK_GREY) 
    for i in range(6): # колл-во линий
        pg.draw.line(screen , WHITE ,[WIDTH/5*i , - HEIGHT], [WIDTH/5*i , HEIGHT], 4)
    all_sprites.draw(screen)
    draw_text(screen, str(score), (WIDTH / 2) + 30, 10) 
    user_name(screen, str(name), (WIDTH / 3) + 30, 10)
    pg.display.flip()  

def run_game_loop(name: str):
    amount_of_life = 3
    running, score, i = True, 0, 0 
    while amount_of_life > 0 and running:
        clock.tick(FPS)
        score += 1
        for event in pg.event.get():  
            if event.type == pg.QUIT:
                running = False
            elif event.key == pg.K_ESCAPE:
                    running = False
        i += 1
        if i > 19:
                i = 0
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
        
        all_sprites.update()
        
        collision = pg.sprite.spritecollide (player,mobs, False, pg.sprite.collide_mask)
        
        if collision:
            collision[0].kill()
            amount_of_life -= 1
            hearts.pop(-1).kill()
        update_game_screen(name=name, score=score)

    db.set(name, score)
    return score
    


def init_score_screen():
    name, is_run = '', True
    while is_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_run = False
            elif event.type == pg.KEYDOWN:
                if event.key in {pg.K_ESCAPE, pg.K_RETURN}:
                    is_run = False
                elif event.key == pg.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode


        screen.fill(BLACK)
        draw_text(screen, 'Введите имя:', WIDTH // 2, HEIGHT // 2) 
        draw_text(screen, name, WIDTH // 2 , HEIGHT // 2 + 20)
        pg.display.flip()

    run_game_loop(name=name)

    return name


name = init_score_screen()

def score_game():
    return(f'Ваш результат : {db.get(name)}')

def top_gamers():
    offset = 0 
    for u_name, u_score in db.get():
        draw_text(screen, (f'{u_name}: {u_score}'), WIDTH // 2, HEIGHT - 200 - offset)
        offset -= 30

game_over_loop = True
while game_over_loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over_loop = False
            elif event.type == pg.KEYDOWN:
                if event.key in {pg.K_ESCAPE, pg.K_RETURN}:
                    game_over_loop = False

        screen.fill(BLACK)
        draw_text(screen, 'Game Over', WIDTH // 2, HEIGHT - 450)
        draw_text(screen, score_game(), WIDTH // 2, HEIGHT // 2) 
        draw_text(screen, 'Best scores:', WIDTH // 2, HEIGHT - 250)
        top_gamers()
        pg.display.flip()

pg.quit()
