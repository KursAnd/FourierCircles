
import numpy as np
import math
import pygame as pg
import sys

class circle_t:
  def __init__ (self, x, y, r):
    self.x = x
    self.y = y
    self.r = r

class config_t:
  def __init__ (self, r, f, w):
    self.r = r
    self.f = f
    self.w = w

  def __lt__ (self, oth):
    if self.r < oth.r:
      return True
    return False


class fourie_circles:
  def __init__ (self, x, y):
    if len(x) != len (y):
      return
    z = [complex(_x, _y) for _x, _y in zip (x, y)]
    M = len (z)
    N = M

    X = np.fft.fft(z, N)
    X_amp = (1/M) * np.abs(X)
    X_phs = np.angle(X)
    X_deg = np.degrees(X_phs)

    W = np.arange(N)
    W = 2 * math.pi * W / N

    print ('N:\t', N)
    print ('z:\t', z)
    print ('X:\t', X)
    print ('X_amp:\t', X_amp)
    print ('X_phs:\t', X_phs)
    print ('X_deg:\t', X_deg)
    print ('w:\t', W)

    self.x = x
    self.y = y
    self.W = W
    self.N = N
    self.conf = [config_t (r, f, w) for r, f, w in zip (X_amp, X_phs, W)]
    self.conf.sort (reverse=True)
    for i in range (len (self.conf)):
      print ('r = ', self.conf[i].r, 'f = ', self.conf[i].f, 'w = ', self.conf[i].w)

  def get_configs (self, step):
    res = []
    x = 0 #np.mean (self.x)
    y = 0 #np.mean (self.y)
    alf = 0
    for el in self.conf:
      res.append (circle_t (x, y, el.r))

      alf = el.f + el.w * step  #math.radians(deg)
      x = x + el.r * math.cos(alf)
      y = y + el.r * math.sin(alf)

    res.append (circle_t (x, y, 0))
    return res




FPS = 1
WIN_WIDTH = 640
WIN_HEIGHT = 640

GREEN    = (0, 200, 64)
WHITE    = (255, 255, 255)
BLACK    = (0, 0, 0)
RED      = (255, 0, 0)
DARK_RED = (128, 0, 0)
SILVER   = (192, 192, 192)
DARKGRAY = (169, 169, 169)
GRAY     = (128, 128, 128)



sc = pg.display.set_mode ((WIN_WIDTH, WIN_HEIGHT))
def clear_display ():
  sc.fill (WHITE)

def draw_picture ():
  x = []
  y = []
  start = False
  while 1:
    for event in pg.event.get ():
      if event.type == pg.QUIT:
        sys.exit (0)
      if event.type == pg.MOUSEMOTION and start:
        x.append (event.pos[0])
        y.append (event.pos[1])
      if event.type == pg.MOUSEBUTTONDOWN:
        if start:
          return x, y
        else:
          start = True

    clear_display ()
    for i in range (len(x)):
      pg.draw.circle (sc, DARK_RED, (x[i], y[i]), 1, 2)
    pg.display.update ()



pg.init()
points_x = []
points_y = []
points_x, points_y = draw_picture ()
fc = fourie_circles (points_x, points_y)
for el in fc.get_configs (0):
  print ('r = ', el.r, 'x = ', el.x, 'y = ', el.y)

step = 0
result_line = []
while True:
  for event in pg.event.get ():
    if event.type == pg.QUIT or event.type == pg.MOUSEBUTTONDOWN:
      sys.exit (0)

  clear_display ()
  circle_centers_line = []
  for el in fc.get_configs (step):
    pg.draw.circle (sc, GRAY, (el.x+200*0, el.y+200*0), el.r, 1)
    circle_centers_line.append ([el.x+200*0, el.y+200*0])

  result_line.append (circle_centers_line[-1])
  pg.draw.aalines (sc, GRAY, False, circle_centers_line)
  
  if len (result_line) > 1:
    pg.draw.aalines (sc, RED, False, result_line)

  for i in range (len(points_x)):
    pg.draw.circle (sc, DARK_RED, (points_x[i]+200*0, points_y[i]+200*0), 1, 2)

  pg.display.update ()
  step = step + 1

  pg.time.delay(50)
