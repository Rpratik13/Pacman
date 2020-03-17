from pygame import joystick, key
from pygame.locals import *
from tiles import Tiles

def checkReverse(current, nxt):
    if current == 'left' and nxt == 'right':
        return True
    elif current == 'right' and nxt == 'left':
        return True
    elif current == 'up' and nxt == 'down':
        return True
    elif current == 'down' and nxt == 'up':
        return True
    return False

class Pacman:
    def __init__(self):
        self.tilepos = (23, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
        self.move = 'right' 
        self.direction = 'r'
        self.nmove = ''
        self.score = 0

    def makeMove(self, tiles):
        rev = {'left':'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'}
        if key.get_pressed()[K_LEFT]:
            if checkReverse(self.move, 'left'):
                self.move = 'left'
            else:
                self.nmove = 'left'
            self.direction = 'l'
        elif key.get_pressed()[K_RIGHT]:
            if checkReverse(self.move, 'right'):
                self.move = 'right'
            else:
                self.nmove = 'right'
            self.direction = 'r'
        elif key.get_pressed()[K_UP]:
            if checkReverse(self.move, 'up'):
                self.move = 'up'
            else:
                self.nmove = 'up'
            self.direction = 'u'
        elif key.get_pressed()[K_DOWN]:
            if checkReverse(self.move, 'down'):
                self.move = 'down'
            else:
                self.nmove = 'down'
            self.direction = 'd'
        # print(self.move)

        if self.tilepos in tiles.nodes and self.nmove != '':
            if self.nmove == 'left' and tiles.tiles[self.tilepos[0]][self.tilepos[1] - 1] != 1:
                self.move = self.nmove
                self.nmove = ''
            elif self.nmove == 'right' and tiles.tiles[self.tilepos[0]][self.tilepos[1] + 1] != 1:
                self.move = self.nmove
                self.nmove = ''
            elif self.nmove == 'up' and tiles.tiles[self.tilepos[0] - 1][self.tilepos[1]] != 1:
                self.move = self.nmove
                self.nmove = ''
            elif self.nmove == 'down' and tiles.tiles[self.tilepos[0] + 1][self.tilepos[1]] != 1:
                self.move = self.nmove
                self.nmove = ''
        
        if self.move == 'left':
            if tiles.tiles[self.tilepos[0]][self.tilepos[1] - 1] != 1:
                if tiles.tiles[self.tilepos[0]][self.tilepos[1] - 1] == 0:
                    self.score += 5
                elif tiles.tiles[self.tilepos[0]][self.tilepos[1] - 1] == 2:
                    self.score += 50
                tiles.tiles[self.tilepos[0]][self.tilepos[1] - 1] = 3
                self.tilepos = (self.tilepos[0], self.tilepos[1] - 1)
           
        elif self.move == 'right':
            if tiles.tiles[self.tilepos[0]][self.tilepos[1] + 1] != 1:
                if tiles.tiles[self.tilepos[0]][self.tilepos[1] + 1] == 0:
                    self.score += 5
                elif tiles.tiles[self.tilepos[0]][self.tilepos[1] + 1] == 2:
                    self.score += 50
                tiles.tiles[self.tilepos[0]][self.tilepos[1] + 1] = 3
                self.tilepos = (self.tilepos[0], self.tilepos[1] + 1)
           
        elif self.move == 'up':
            if tiles.tiles[self.tilepos[0] - 1][self.tilepos[1]] != 1:
                if tiles.tiles[self.tilepos[0] - 1][self.tilepos[1]] == 0:
                    self.score += 5
                elif tiles.tiles[self.tilepos[0] - 1][self.tilepos[1]] == 2:
                    self.score += 50
                tiles.tiles[self.tilepos[0] - 1][self.tilepos[1]] = 3
                self.tilepos = (self.tilepos[0] - 1, self.tilepos[1])
           
        elif self.move == 'down':
            if tiles.tiles[self.tilepos[0] + 1][self.tilepos[1]] != 1:
                if tiles.tiles[self.tilepos[0] + 1][self.tilepos[1]] == 0:
                    self.score += 5
                elif tiles.tiles[self.tilepos[0] + 1][self.tilepos[1]] == 2:
                    self.score += 50
                tiles.tiles[self.tilepos[0] + 1][self.tilepos[1]] = 3
                self.tilepos = (self.tilepos[0] + 1, self.tilepos[1])
           
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8) 