from pygame import joystick, key
from pygame.locals import *

joystick.init()


while True:    
    if key.get_pressed()[K_LEFT]:
        print(key.get_pressed())
        p.angle = 180
        p.movex = -20
    if key.get_pressed()[K_RIGHT]:
        p.angle = 0
        p.movex = 20
    if key.get_pressed()[K_UP]:
        p.angle = 90
        p.movey = -20
    if key.get_pressed()[K_DOWN]:
        p.angle = 270
        p.movey = 20
    
    
