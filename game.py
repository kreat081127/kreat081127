import pygame as pg
pg.init()
font_name = pg.font.match_font('Arial') #поиск шрифта
size = 18 #его размер

w,h = 600,600
win = pg.display.set_mode((w,h))

# image = pg.image.load('pngwing.png') #загрузка (добавление) картинки
# image = pg.transform.scale(image, (w,h)) #изменение картинки на полный экран
name = ''
def draw_text(surf, text, x, y, size=size, color=(255,255,255)):
  font = pg.font.Font(font_name, size) #определение шрифта
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x,y)
  surf.blit(text_surface, text_rect)
def user_name(surf,text,x,y,size):
  font = pg.font.Font(font_name, size)  # определение шрифта
  text_surface = font.render(text, True, color=(255,255,255))
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)
fps = pg.time.Clock
main = True
while main:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()
    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_BACKSPACE:
        name = name[:-1]
      elif event.key == pg.K_RETURN:
        main = False
      else:
        name += event.unicode
  win.fill((0,0,0))
  # win.blit(image, (0, 0)) #добавление картинки в игру
  draw_text(win, 'Введите имя:', (w//2),(h//2))
  draw_text(win, name, 300,325)
  pg.display.update()


while True:
  for i in pg.event.get():
    if i.type == pg.QUIT:
      exit()
  win.fill((119,0,255))
  for y in range(0,h,10):
    for x in range(0,w,10):
      pg.draw.line(win,(0,0,0), (0,y),(w,y))
      pg.draw.line(win, (0,0,0), (x, 0), (x, h))
  pg.display.update()

draw_text(win, name, 15, 15, color=(0,0,0))
draw_text(win, f'Score:{score}', WIDTH // 2, 15,color=(0,0,0))

collision = pg.sprite.spritecollide(player,apple_sprites, False, pg.sprite.collide_mask) 
if collision:
    score += 1
    apple.new_pos()

class Tail(pg.sprite.Sprite):
  def __init__(self):
    super().__init__(*group)
    self.speed_x = player.speed_x
    self.speed_y = player.speed_y
    self_image = pg.image.load('')
    self.rect 
