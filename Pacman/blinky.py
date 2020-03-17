import random

class Blinky:
    def __init__(self):
        self.tilepos = (14, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
        self.move_seq = []
        self.mode = 'chase'
        self.count = 0
        self.scattertime = 0
        self.frightentime = 0
        self.direction = 'u'
        self.color = 'red'
    
    def reset(self):
        self.tilepos = (14, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
        self.move_seq = []
        self.mode = 'chase'
        self.count = -11
        self.scattertime = 0
        self.frightentime = 0
        self.direction = 'u'
        self.color = 'red'

    def getout(self):
        self.tilepos = (self.tilepos[0] - 1, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)

    def shortestNodesP(self, mode, player, tiles):
        positions = [player.tilepos, self.tilepos]
        flag = True
        for i in positions:
            reachable = []
            left = (100, 100)
            right = (100, 100)
            up = (100, 100)
            down = (100, 100)
            for j in tiles.nodes:
                if i == j and flag:
                    reachable.append(j)


                if i[0] == j[0]:
                    if tiles.tiles[int(i[0])][int(i[1] - 1)] != 1:
                        if i[1] > j[1] and i[1] - j[1] < abs(left[1] - i[1]) and (flag or self.direction != 'r'):
                            left = j
                    if tiles.tiles[int(i[0])][int(i[1] + 1)] != 1:
                        if i[1] < j[1] and j[1] - i[1] < abs(right[1] - i[1]) and (flag or self.direction != 'l'):
                            right = j

                if i[1] == j[1]:
                    if tiles.tiles[int(i[0] - 1)][int(i[1])] != 1:
                        if i[0] > j[0] and i[0] - j[0] < abs(up[0] - i[0]) and (flag or self.direction != 'd'):
                            up = j
                    if tiles.tiles[int(i[0] + 1)][int(i[1])] != 1:
                        if i[0] < j[0] and j[0] - i[0] < abs(down[0] - i[0]) and (flag or self.direction != 'u'):
                            down = j
            reachable.extend([left, right, up, down])

            while (100, 100) in reachable:
                reachable.remove((100, 100))
            if flag:
                if player.tilepos in reachable:
                    player.breachable = [player.tilepos]
                else:
                    player.breachable = reachable
                flag = False
            else:
                self.reachable = reachable
        if mode == 'chase':
            return player.breachable
        elif mode == 'scatter':
            return [(1, 1)]

    def AstarSearch(self, start, end, tiles):
        move_seq = [start]
        currentNode = start
        while currentNode != end:
            heur = float('inf')
            for i in tiles.reachable_nodes[currentNode]:
                temp = tiles.node_distance[currentNode][tiles.nodes.index(i)] + tiles.node_distance[i][tiles.nodes.index(end)]

                if temp < heur:
                    heur = temp
                    next_node = i
            move_seq.append(next_node)
            currentNode = next_node
        return move_seq

    def move(self, player, tiles):
        if self.scattertime == 0 and self.frightentime == 0:
            self.mode = 'chase'
            self.color = 'red'
        self.scattertime = max(self.scattertime - 1, 0)
        self.frightentime = max(self.frightentime - 1, 0)
        self.count += 1
        if self.count in range(7, 10):
            self.getout()
        elif self.count > 10:
            if (self.count - 10) % 40 == 0:
                self.mode = 'scatter'
                self.scattertime = 8

            if self.mode == 'chase':
                breachable = self.shortestNodesP('chase', player, tiles)
            elif self.mode == 'scatter':
                breachable = self.shortestNodesP('scatter', player, tiles)
            elif self.mode == 'frightened':
                breachable = self.shortestNodesP('chase', player, tiles)
                self.move_seq = [random.choice(self.reachable)]
                self.color = 'blue'
                



            if self.mode != 'frightened':
                dist = float('inf')
                for i in self.reachable:
                    blinky_dist = abs(i[0] - self.tilepos[0]) + abs(i[1] - self.tilepos[1])
                    for j in breachable:
                        if abs(self.tilepos[0] - player.tilepos[0]) + abs(self.tilepos[1] - player.tilepos[1]) <= 4:
                            player_dist = 0
                        else:
                            player_dist = abs(j[0] - player.tilepos[0]) + abs(j[1] - player.tilepos[1])


                        if blinky_dist + player_dist + tiles.node_distance[i][tiles.nodes.index(j)] < dist:
                            dist =  blinky_dist + player_dist + tiles.node_distance[i][tiles.nodes.index(j)]
                            start = i
                            end = j

                   
                    move_seq = self.AstarSearch(start, end, tiles)
                    if player.tilepos != move_seq[-1] and abs(self.tilepos[0] - player.tilepos[0]) + abs(self.tilepos[1] - player.tilepos[1]) > 8:
                        if self.mode == 'chase':
                            move_seq.append(player.tilepos)
                    self.move_seq = move_seq
            if self.move_seq[0][0] == self.tilepos[0]:
                if self.move_seq[0][1] < self.tilepos[1]:
                    self.tilepos = (self.tilepos[0], self.tilepos[1] - 1)
                    self.direction = 'l'
                else:
                    self.tilepos = (self.tilepos[0], self.tilepos[1] + 1)
                    self.direction = 'r'
            else:
                if self.move_seq[0][0] < self.tilepos[0]:
                    self.tilepos = (self.tilepos[0] - 1, self.tilepos[1])
                    self.direction = 'u'
                else:
                    self.tilepos = (self.tilepos[0] + 1, self.tilepos[1])
                    self.direction = 'd'
            self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
            
