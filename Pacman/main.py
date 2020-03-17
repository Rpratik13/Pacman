import pgzrun
from pygame import *
from blinky import *
from pinky import * 
from tiles import *
from pygame import joystick, key
from pacman import *
from clyde import *
from inky import *
import time



WIDTH = 448
HEIGHT = 496


global player, tiles, count, flag, ghost_move, game, stime
stime = 0.055
game = 0
ghost_move = 2 
flag = False
count = 0





def init():
    global blinky, pinky, clyde, player, tiles, inky
    player = Pacman()
    blinky = Blinky()
    pinky = Pinky()
    clyde = Clyde()
    inky = Inky()
    tiles = Tiles()
    # music.play('test.mp3')

def draw():
    global tiles, game, ghost_move, hscore
    f = open('high.txt', 'r')
    hscore = int(f.read())
    f.close()

    screen.blit('map1', (0, 0))
    if game != 1:
        screen.draw.filled_circle(player.pos, 10, "yellow")
    screen.draw.filled_circle(blinky.pos, 10, blinky.color)
    screen.draw.filled_circle(pinky.pos, 10, pinky.color)
    screen.draw.filled_circle(inky.pos, 10, inky.color)
    screen.draw.filled_circle(clyde.pos, 10, clyde.color)
    screen.draw.text("SCORE\n"+str(player.score), (15, 200), color='white')
    screen.draw.text("HIGH\nSCORE\n"+str(hscore), (385, 200), color='white')
    if game == 1:
        screen.draw.text("Game Over", (185, 280), color="red")
        if player.score > hscore:
            f = open('high.txt', 'w')
            f.write(str(player.score))
            f.close()
    elif game == 2:
        screen.draw.text("You Win!", (185, 280), color="Yellow")

    for i in range(len(tiles.tiles)):
            for j in range(len(tiles.tiles[0])):
                if tiles.tiles[i][j] == 0:
                    screen.draw.circle((8 + j * 16, 8 + i * 16), 1, 'yellow')
                elif tiles.tiles[i][j] == 2:
                    screen.draw.filled_circle((8 + j * 16, 8 + i * 16), 4, 'yellow')
    # for i in tiles.nodes:
    #     screen.draw.filled_circle((8 + i[1] * 16, 8 + i[0] * 16), 4, 'red')

    # if ghost_move == 2:
    # move_seq = [blinky.tilepos]
    # move_seq.extend(blinky.move_seq)

    # for i in range(len(move_seq) - 1):
    #     screen.draw.line((8 + move_seq[i][1] * 16, 8 + move_seq[i][0] * 16), (8 + move_seq[i + 1][1] * 16, 8 + move_seq[i + 1][0] * 16), 'red')

    # move_seq = [pinky.tilepos]
    # move_seq.extend(pinky.move_seq)
    # for i in range(len(move_seq) - 1):
    #     screen.draw.line((8 + move_seq[i][1] * 16, 8 + move_seq[i][0] * 16), (8 + move_seq[i + 1][1] * 16, 8 + move_seq[i + 1][0] * 16), 'pink')

    # move_seq = [inky.tilepos]
    # move_seq.extend(inky.move_seq)
    # for i in range(len(move_seq) - 1):
    #     screen.draw.line((8 + move_seq[i][1] * 16, 8 + move_seq[i][0] * 16), (8 + move_seq[i + 1][1] * 16, 8 + move_seq[i + 1][0] * 16), "#00FFFF")

    # move_seq = [clyde.tilepos]

    # move_seq.extend(clyde.move_seq)
    # if (abs(clyde.tilepos[0] - player.tilepos[0]) + abs(clyde.tilepos[1] - player.tilepos[1])) <= 8 and (player.tilepos in move_seq):
    #         move_seq.remove(player.tilepos)
    # for i in range(len(move_seq) - 1):
    #     screen.draw.line((8 + move_seq[i][1] * 16, 8 + move_seq[i][0] * 16), (8 + move_seq[i + 1][1] * 16, 8 + move_seq[i + 1][0] * 16), 'orange')



def update():


    global count, flag, ghost_move, game, stime

    
    if tiles.checkGame():
        game = 5

    if game == 5:
        stime = max(0, stime - 0.01)
        game = 2

    if game == 0:
        if key.get_pressed()[K_SPACE]:
            flag = True
        if flag:
            
            time.sleep(stime)
            if ghost_move == 2:
                player.makeMove(tiles)
                if player.tilepos in tiles.super:
                    tiles.super.remove(player.tilepos)
                    pinky.mode = 'frightened'
                    blinky.mode = 'frightened'
                    clyde.mode   = 'frightened'
                    inky.mode = 'frightened'
                    blinky.frightentime = 40
                    blinky.color = 'blue'
                    pinky.frightentime = 40
                    pinky.color = 'blue'
                    inky.frightentime = 40
                    inky.color = 'blue'
                    clyde.frightentime = 40
                    clyde.color = 'blue'
                
                # pinky.move(player, tiles)
                # print(blinky.mode)
                
                # clyde.move(player, tiles)
                if player.tilepos == blinky.tilepos:
                    if blinky.frightentime > 0:   
                        blinky.reset()
                        player.score += 200
                    else:
                        game = 1
                if player.tilepos == pinky.tilepos:
                    if pinky.frightentime > 0:   
                        pinky.reset()
                        player.score += 200
                    else:
                        game = 1
                if player.tilepos == inky.tilepos:
                    if inky.frightentime > 0:   
                        inky.reset()
                        player.score += 200
                    else:
                        game = 1
                if player.tilepos == clyde.tilepos:
                    if clyde.frightentime > 0:   
                        clyde.reset()
                        player.score += 200
                    else:
                        game = 1

                blinky.move(player, tiles)
                pinky.move(player, tiles)
                inky.move(player, tiles, blinky)
                clyde.move(player, tiles)
                # print(blinky.mode)
                if player.tilepos == blinky.tilepos:
                    if blinky.frightentime > 0:   
                        blinky.reset()
                        player.score += 200
                    else:
                        game = 1
                
                if player.tilepos == pinky.tilepos:
                    if pinky.frightentime > 0:   
                        pinky.reset()
                        player.score += 200
                    else:
                        game = 1
                if player.tilepos == inky.tilepos:
                    if inky.frightentime > 0:   
                        inky.reset()
                        player.score += 200
                    else:
                        game = 1
                if player.tilepos == clyde.tilepos:
                    if clyde.frightentime > 0:   
                        clyde.reset()
                        player.score += 200
                    else:
                        game = 1
                ghost_move = 0
            ghost_move += 1

            
  
    else:
        if key.get_pressed()[K_SPACE]:
            last_game = game
            if game == 2:
                temp = player.score
            game = 0
            init()
            if last_game == 2:
                player.score = temp


init()
pgzrun.go()