import pygame as py
py.init()
font_name = py.font.match_font('Arial') #поиск шрифта
size = 18 #его размер

w,h = 600,600
win = py.display.set_mode((w,h))

image = py.image.load('pngwing.png') #загрузка (добавление) картинки
image = py.transform.scale(image, (w,h)) #изменение картинки на полный экран

name = ''
def draw_text(surf, text, x, y, size=size, color=(255,255,255)):
  font = py.font.Font(font_name, size) #определение шрифта
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x,y)
  surf.blit(text_surface, text_rect)
def user_name(surf,text,x,y,size):
  font = py.font.Font(font_name, size)  # определение шрифта
  text_surface = font.render(text, True, color=(255,255,255))
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)
fps = py.time.Clock
while 1:
  for event in py.event.get():
    if event.type == py.QUIT:
      exit()
    elif event.type == py.KEYDOWN:
      if event.key == py.K_BACKSPACE:
        name = name[:-1]
      elif event.key == py.K_RETURN:
        print(name)
        name = ''
      else:
        name += event.unicode
  win.fill((0,0,0))
  win.blit(image, (0, 0)) #добавление картинки в игру
  draw_text(win, 'Введите имя:', (w//2),(h//2))
  draw_text(win, name, 300,325)
  py.display.update()
  py.time.delay(10)
