import random

class Pinky:
    def __init__(self):
        self.tilepos = (14, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
        self.move_seq = []
        self.mode = 'chase'
        self.count = 0
        self.scattertime = 0
        self.frightentime = 0
        self.direction = 'u'
        self.color = 'pink'

    def getout(self):
        self.tilepos = (self.tilepos[0] - 1, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
    
    def reset(self):
        self.tilepos = (14, 13)
        self.pos = (self.tilepos[1] * 16 + 8, self.tilepos[0] * 16 + 8)
        self.move_seq = []
        self.mode = 'chase'
        self.count = 18
        self.scattertime = 0
        self.frightentime = 0
        self.direction = 'u'
        self.color = 'pink'

    def calcForward(self, player, tiles):
        dist = 5
        while True:
            if player.direction == 'l':
                move = (0, -dist)
            elif player.direction == 'r':
                move = (0, dist)
            elif player.direction == 'u':
                move = (-dist, 0)
            elif player.direction == 'd':
                move = (dist, 0)
            x = player.tilepos[0] + move[0]
            y = player.tilepos[1] + move[1]
            if x in range(0, 30) and y in range(0, 27) and tiles.tiles[x][y] != 1:
                return (x, y)
            dist -= 1  
    def shortestNodesP(self, mode, player, tiles):
        for_position = self.calcForward(player, tiles)
        positions = [for_position, self.tilepos]
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
                    if tiles.tiles[int(i[0])][int(i[1] - 1)] != 1 and self.direction != 'r':
                        if i[1] > j[1] and i[1] - j[1] < abs(left[1] - i[1]):
                            left = j
                    if tiles.tiles[int(i[0])][int(i[1] + 1)] != 1 and self.direction != 'l':
                        if i[1] < j[1] and j[1] - i[1] < abs(right[1] - i[1]):
                            right = j

                if i[1] == j[1]:
                    if tiles.tiles[int(i[0] - 1)][int(i[1])] != 1 and self.direction != 'd':
                        if i[0] > j[0] and i[0] - j[0] < abs(up[0] - i[0]):
                            up = j
                    if tiles.tiles[int(i[0] + 1)][int(i[1])] != 1 and self.direction != 'u':
                        if i[0] < j[0] and j[0] - i[0] < abs(down[0] - i[0]):
                            down = j
            reachable.extend([left, right, up, down])

            while (100, 100) in reachable:
                reachable.remove((100, 100))
            if flag:
                if for_position in reachable:
                    player.pinkyreachable = [for_position]
                else:
                    player.pinkyreachable = reachable
                flag = False
            else:
                self.reachable = reachable
        if mode == 'chase':
            return player.pinkyreachable
        elif mode == 'scatter':
            return [(1, 26)]

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
            self.color = 'pink'
        self.scattertime = max(self.scattertime - 1, 0)
        self.frightentime = max(self.frightentime - 1, 0)
        self.count += 1
        if self.count in range(27, 30):
            self.getout()
        elif self.count > 30:
            if (self.count - 30) % 50 == 0:
                self.mode = 'scatter'
                self.scattertime = 8

            if self.mode == 'chase':
                preachable = self.shortestNodesP('chase', player, tiles)
            elif self.mode == 'scatter':
                preachable = self.shortestNodesP('scatter', player, tiles)
            elif self.mode == 'frightened':
                preachable = self.shortestNodesP('chase', player, tiles)
                self.move_seq = [random.choice(self.reachable)]
                self.color = 'blue'
            if self.mode != 'frightened':
                dist = float('inf')
                for i in self.reachable:
                    pinky_dist = abs(i[0] - self.tilepos[0]) + abs(i[1] - self.tilepos[1])
                    for j in preachable:
                        player_dist = abs(j[0] - player.tilepos[0]) + abs(j[1] - player.tilepos[1])


                        if pinky_dist + player_dist + tiles.node_distance[i][tiles.nodes.index(j)] < dist:
                            dist =  pinky_dist + player_dist + tiles.node_distance[i][tiles.nodes.index(j)]
                            start = i
                            end = j

                    move_seq = self.AstarSearch(start, end, tiles)
                    if player.tilepos != move_seq[-1] and self.mode == 'chase':
                        move_seq.append(self.calcForward(player, tiles))

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
            
