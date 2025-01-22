#
# MiniMario.py 2025/1/22
#
import pyxel
import random

START_STAGEMAP = 0 # 0～7
START_ROUND = 0 # 0～2
STATUS_TITLE, STATUS_OPENING, STATUS_PLAY, STATUS_PAUSE, STATUS_ENDING, STATUS_GAMEOVER = 1, 2, 3, 4, 5, 6
GOAL_BEGIN, GOAL_STOP, GOAL_JUMP = 11, 12, 13
START_TIME = 6000
MAX_STAGE = 8
MAX_ROUND = 3
# MapX, MapY, PlayerX, PlayerY, BackgroundColor, NextStage, Warp
STAGE_MAP = ((0,0,16*1,16*13,pyxel.COLOR_LIGHT_BLUE, 1, ( 8,)),            #  0,stage1-1(1-1)
             (0,1,16*1,16*1 ,pyxel.COLOR_BLACK,      2, (10,12,13)),       #  1,stage2-1(1-2)
             (0,2,16*1,16*13,pyxel.COLOR_LIGHT_BLUE, 3, (14,)),            #  2,stage3-1(5-2)
             (0,3,16*1,16*1 ,pyxel.COLOR_BLACK,      4, (16,18,19)),       #  3,stage4-1(4-2)
             (0,4,16*1,16*13,pyxel.COLOR_LIGHT_BLUE, 5, (20,)),            #  4,stage5-1(6-1)
             (0,5,16*1,16*13,pyxel.COLOR_LIGHT_BLUE, 6, (22,24,26,28)),    #  5,stage6-1(6-2)
             (0,6,16*1,16*13,pyxel.COLOR_LIGHT_BLUE, 7, (30,)),            #  6,stage7-1(7-1)
             (5,7,8*3 ,16*11,pyxel.COLOR_BLACK,      0, (32,32,32,32,32)), #  7,stage8-1
             
             (0,7,16*1,16*1 ,pyxel.COLOR_BLACK,      1, ( 9, 9, 9, 9, 9)), #  8,stage1-2
             (6,0,8*11,16*11,pyxel.COLOR_LIGHT_BLUE, 1, ( 8,)),            #  9,stage1-1a
             
             (1,7,16*1,16*1 ,pyxel.COLOR_BLACK,      2, (11,11,11,11,11)), # 10,stage2-2
             (5,1,8*5 ,16*10,pyxel.COLOR_BLACK,      2, (10,12,13)),       # 11,stage2-1a
             (7,7,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 2, (11,11,11,11,11)), # 12,stage2-3
             (7,7,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 3, (11,11,11,11,11)), # 13,stage2-4
             
             (2,7,16*1,16*1 ,pyxel.COLOR_BLACK,      3, (15,15,15,15,15)), # 14,stage3-2
             (4,2,8*15,16*11,pyxel.COLOR_LIGHT_BLUE, 3, (14,)),            # 15,stage3-1a
             
             (3,7,16*1,16*1 ,pyxel.COLOR_BLACK,      4, (17,17,17,17,17)), # 16,stage4-2
             (4,3,16*9,16*10,pyxel.COLOR_BLACK,      4, (16,18,19)),       # 17,stage4-1a
             (7,7,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 4, (17,17,17,17,17)), # 18,stage4-3
             (7,7,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 5, (17,17,17,17,17)), # 19,stage4-4
             
             (4,7,16*1,16*1 ,pyxel.COLOR_BLACK,      4, (21,21,21,21,21)), # 20,stage5-2
             (4,4,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 5, (20,)),            # 21,stage5-1a
             
             (3,7,16*1,16*1 ,pyxel.COLOR_BLACK,      6, (23,23,23,23,23)), # 22,stage6-2
             (1,5,8*13,16*11,pyxel.COLOR_LIGHT_BLUE, 6, (22,24,26,28)),    # 23,stage6-1a
             (1,7,16*1,16*1 ,pyxel.COLOR_BLACK,      6, (25,25,25,25,25)), # 24,stage6-3
             (3,5,8*7 ,16*11,pyxel.COLOR_LIGHT_BLUE, 6, (22,24,26,28)),    # 25,stage6-1b
             (2,7,16*1,16*1 ,pyxel.COLOR_BLACK,      6, (27,27,27,27,27)), # 26,stage6-4
             (4,5,8*7 ,16*10,pyxel.COLOR_LIGHT_BLUE, 6, (22,24,26,28)),    # 27,stage6-1c
             (4,7,16*1,16*1 ,pyxel.COLOR_BLACK,      6, (29,29,29,29,29)), # 28,stage6-5
             (6,5,8*19,16*6 ,pyxel.COLOR_LIGHT_BLUE, 6, (22,24,26,28)),    # 29,stage6-1d
             
             (4,7,16*2,16*1 ,pyxel.COLOR_BLACK,      7, (31,31,31,31,31)), # 30,stage7-2
             (5,6,8*9 ,16*11,pyxel.COLOR_LIGHT_BLUE, 7, (30,)),            # 31,stage7-1a
             
             (7,7,0   ,16*1 ,pyxel.COLOR_LIGHT_BLUE, 0, ( 7, 7, 7, 7, 7)), # 32,stage8-1a
             )

RET_NONE, RET_SCREENOUT, RET_ATTACK, RET_STOMPED, RET_TOUCH, RET_BOUNCE = 0, 1, 2, 3, 4, 5
Y_SHIFT  = 12
OUTLOOK  = 4
WAITTIME = 30
INVULNERABLETIME = 60
NOMOVE = (( 1,0), 
          ( 0,2),( 1,2),( 0,3),( 1,3),  # BLOCK1 \
          ( 2,2),( 2,3),                # BRICK_NORMAL \
          ( 4,2),( 5,2),( 4,3),( 5,3),  # QUESTION_COIN, 68,69,100,101, \
          ( 6,2),( 7,2),( 6,3),( 7,3),  # EMPTY_BLOCK, 70,71,102,103, \
          ( 8,2),( 9,2),( 8,3),( 9,3),  # BLOCK2, 72,73,104,105, \
          (10,2),(11,2),(10,3),(11,3),  # HODAI1, 74,75,106,107, \
          (12,2),(13,2),(12,3),(13,3),  # HODAI2, 76,77,108,109, \
          (14,2),(15,2),                # HODAI3, 78,79, \
          (16,2),(17,2),(16,3),(17,3),  # PIPE1, 80,81,112,113, \
          (18,2),(19,2),(18,3),(19,3),  # PIPE2, 82,83,114,115, \
          (20,2),(21,2),(20,3),(21,3),  # PIPE3, 84,85,116,117, \
          (22,2),(23,2),(22,3),(23,3))  # PIPE4, 86,87,118,119)
WARPPIPE = ((26,  2), (27,  2), (26,  3), (27,  3))  # (90, 91, 122, 123)
GOAL     = ((28,  0), (29,  0), (28,  1), (29,  1), (30,  0), (31,  0), (30,  1), (31,  1))  # (28,29,60,61, 30,31,62,63)
KINOPIO  = ((26,  5), (27,  5), (26,  6), (27,  6), (26,  7), (27,  7))  # (186,187,218,219,250,251)
PEACH    = ((24,  5), (25,  5), (24,  6), (25,  6), (24,  7), (25,  7))  # (184,185,216,217,248,249)
BRICK_NORMAL      = (( 2,  2), ( 2,  3)) # , (3, 2), (3, 3))  # ( 66, 98, 67, 99)
EMPTY_BLOCK       = (( 6,  2), ( 7,  2), ( 6,  3), ( 7,  3))  # ( 70, 71,102,103)
BRICK_COIN        = (( 0, 12), ( 1, 12), ( 0, 13), ( 1, 13))  # (384,385,416,417)
BRICK_MUSHROOM    = (( 2, 12), ( 3, 12), ( 2, 13), ( 3, 13))  # (386,387,418,419)
QUESTION_COIN     = (( 4,  2), ( 5,  2), ( 4,  3), ( 5,  3))  # ( 68, 69,100,101)
QUESTION_MUSHROOM = (( 6, 12), ( 7, 12), ( 6, 13), ( 7, 13))  # (390,391,422,423)
HIDDEN_COIN       = (( 8, 12), ( 9, 12), ( 8, 13), ( 9, 13))  # (392,393,424,425)
HIDDEN_MUSHROOM   = ((10, 12), (11, 12), (10, 13), (11, 13))  # (394,395,426,427)
HIDDEN_ALL        = (( 8, 12), ( 9, 12), ( 8, 13), ( 9, 13), (10, 12), (11, 12), (10, 13), (11, 13))  #(392,393,424,425, 394,395,426,427)
MAP_COIN          = (( 0,  8), ( 1,  8), ( 0,  9), ( 1,  9))  # (256,257,288,289)
ITEM_BREAK, ITEM_EMPTY, ITEM_COIN, ITEM_MUSHROOM = 0, 1, 2, 3
CHARA_RUN = (2, 3, 4, 3)
CHARA_BRAKE, CHARA_JUMP, CHARA_GAMEOVER = 5, 6, 7
CHARA_KURIBO  = (8, 4)  # 136
CHARA_TOGEZO  = ((4, 4), (6, 4))  # (132, 134)
CHARA_HODAI   = (10, 2)  # 74
CHARA_KUPPA   = ((12, 4), (16, 4))# (140, 144)
CHARA_KINOPIO = (26, 5)  # 186
CHARA_PEACH   = (24, 5)  # 184

class App:
    map = [[0]*256 for i in range(256)]
    score = 0
    coins = 0
    lives = 3
    kuribo = []
    togezo = []
    kuppa = []
    hodaikiller = []
    brick = []
    question = []
    rescue = []
    stage = stagemap = START_STAGEMAP
    nextstagemap = 0
    round = START_ROUND
    issupermario = 0
    istimestop = 1
    remaintime = 0
    status = STATUS_TITLE

    def __init__(self):
        pyxel.init(32*8, 32*8, title='Mini Mario 1.1')
        pyxel.load('assets/MiniMario.pyxres')
        pyxel.mouse(True)
        for y in range(256):
            for x in range(256):
                self.map[x][y] = pyxel.tilemaps[0].pget(x, y)
                if self.map[x][y] == CHARA_KURIBO:
                    pyxel.tilemaps[0].pset(x,   y,   (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y,   (0, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
                    if self.round == 1:
                        self.togezo.append(Togezo(x*8, y*8))
                    elif self.round>1 and x<254 and y>2 and \
                            self.map[x][y-2]==0 and self.map[x+2][y-2]==0 and self.map[x+2][y]==0:
                        self.kuppa.append(Kuppa(x*8, y*8-16))
                    else:
                        self.kuribo.append(Kuribo(x*8, y*8))
                elif self.map[x][y] in CHARA_TOGEZO:
                    self.togezo.append(Togezo(x*8, y*8))
                    pyxel.tilemaps[0].pset(x,   y,   (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y,   (0, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
                elif self.map[x][y] in CHARA_KUPPA:
                    self.kuppa.append(Kuppa(x*8, y*8))
                    for x1 in range(4):
                        for y1 in range(4):
                            pyxel.tilemaps[0].pset(x+x1, y+y1, (0, 0))
                elif self.map[x][y] == CHARA_HODAI:
                    self.hodaikiller.append(HodaiKiller(x*8, y*8))
                elif self.map[x][y] == WARPPIPE[0]:
                    pyxel.tilemaps[0].pset(x,   y,   ( 81%32,  81//32))
                    pyxel.tilemaps[0].pset(x+1, y,   ( 82%32,  82//32))
                    pyxel.tilemaps[0].pset(x,   y+1, (113%32, 113//32))
                    pyxel.tilemaps[0].pset(x+1, y+1, (114%32, 114//32))
                elif self.map[x][y] == CHARA_KINOPIO or self.map[x][y] == CHARA_PEACH:
                    self.rescue.append(Rescue(x*8, y*8))
                    pyxel.tilemaps[0].pset(x,   y,   (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y,   (0, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
                    pyxel.tilemaps[0].pset(x,   y+2, (0, 0))
                    pyxel.tilemaps[0].pset(x+1, y+2, (0, 0))
        self.setdemomap()
        pyxel.run(self.update, self.draw)

    def start(self):
        self.map_x  = STAGE_MAP[self.stagemap][0]*256
        self.map_y8 = STAGE_MAP[self.stagemap][1]*32
        self.player_x = STAGE_MAP[self.stagemap][2]
        self.player_y = STAGE_MAP[self.stagemap][3]
        self.runptn = 0
        self.isgameover = 0
        self.isgoal = 0
        self.isrescue = 0
        self.iswarp = 0
        self.dirct = 1
        self.isjump = 1
        self.isrun = 0
        self.isjumpkey = 1
        self.dx = 0
        self.dy = 0
        self.randomkiller = []
        self.firebreath = []
        self.mushroom = None
        self.blockcoin = None
        self.istimestop = 0
        self.isinvulnerable = 0

        self.warp_xy = []
        for x in range(256):
            for y in range(16):
                if self.map[x][self.map_y8+y*2] == WARPPIPE[0]:
                    self.warp_xy.append([x, self.map_y8+y*2])

        for y in range(STAGE_MAP[self.stagemap][1]*32, STAGE_MAP[self.stagemap][1]*32+32, 2):
            for x in range(max(STAGE_MAP[self.stagemap][0]*32-16, 0), min(STAGE_MAP[self.stagemap][0]*32+32+16, 256), 2):
                self.sethiddenitem(x, y)
        for i in range(len(self.kuribo)):
            self.kuribo[i].reset()
            if self.kuribo[i].init_y//256 == STAGE_MAP[self.stagemap][1] \
                    and STAGE_MAP[self.stagemap][0]*256 <= self.kuribo[i].init_x < STAGE_MAP[self.stagemap][0]*256+256+16*2:
                self.kuribo[i].alive = 1
                self.kuribo[i].dx = 1 if self.kuribo[i].init_x < self.player_x+self.map_x else -1
        for i in range(len(self.togezo)):
            self.togezo[i].reset()
            if self.togezo[i].init_y//256 == STAGE_MAP[self.stagemap][1] \
                    and STAGE_MAP[self.stagemap][0]*256 <= self.togezo[i].init_x < STAGE_MAP[self.stagemap][0]*256+256+16*2:
                self.togezo[i].alive = 1
                self.togezo[i].dx = 1 if self.togezo[i].init_x < self.player_x+self.map_x else -1
        for i in range(len(self.kuppa)):
            self.kuppa[i].reset()
            if self.kuppa[i].init_y//256 == STAGE_MAP[self.stagemap][1] \
                    and STAGE_MAP[self.stagemap][0]*256 <= self.kuppa[i].init_x < STAGE_MAP[self.stagemap][0]*256+256+16*2:
                self.kuppa[i].alive = 1
                self.kuppa[i].dx = 1 if self.kuppa[i].init_x < self.player_x+self.map_x else -1
        for i in range(len(self.hodaikiller)):
            self.hodaikiller[i].reset()

        for i in range(len(self.rescue)):
            self.rescue[i].reset()
            if self.rescue[i].init_y//256 == STAGE_MAP[self.stagemap][1] \
                    and STAGE_MAP[self.stagemap][0]*256 <= self.rescue[i].init_x < STAGE_MAP[self.stagemap][0]*256+256+16*2:
                self.rescue[i].alive = 1

        pyxel.stop()
        pyxel.play(0, 5)

    def roundup(self):
        self.round += 1
        if self.round == 1:
            for i in reversed(range(len(self.kuribo))):
                self.togezo.append(Togezo(self.kuribo[i].init_x, self.kuribo[i].init_y))
                del self.kuribo[i]
        elif self.round > 1:
            self.round = 2
            for i in reversed(range(len(self.kuribo))):
                self.togezo.append(Togezo(self.kuribo[i].init_x, self.kuribo[i].init_y))
                del self.kuribo[i]
            for i in reversed(range(len(self.togezo))):
                self.kuppa.append(Kuppa(self.togezo[i].init_x, self.togezo[i].init_y-16))
                del self.togezo[i]

    def gettilemap(self, x, y):
        if x < 0 or x >= 256*8 or y < 0 or y >= 256:
            return -1
        return pyxel.tilemaps[0].pget(x//8, self.map_y8+y//8)

    def getmap(self, x, y):
        if x<0 or x>=256*8 or y<0 or y>=256:
            return -1
        return self.map[x//8][self.map_y8+y//8]

    def sethiddenitem(self, x, y):
        if 0 <= x < 256 and 0 <= y < 256:
            if self.map[x][y] == BRICK_NORMAL[0] or self.map[x][y] == BRICK_COIN[0] \
                    or self.map[x][y] == BRICK_MUSHROOM[0]:
                pyxel.tilemaps[0].pset(x  , y  , BRICK_NORMAL[0])
                pyxel.tilemaps[0].pset(x+1, y  , BRICK_NORMAL[0])
                pyxel.tilemaps[0].pset(x  , y+1, BRICK_NORMAL[1])
                pyxel.tilemaps[0].pset(x+1, y+1, BRICK_NORMAL[1])
            if self.map[x][y] == QUESTION_COIN[0] or self.map[x][y] == QUESTION_MUSHROOM[0]:
                pyxel.tilemaps[0].pset(x  , y  , QUESTION_COIN[0])
                pyxel.tilemaps[0].pset(x+1, y  , QUESTION_COIN[1])
                pyxel.tilemaps[0].pset(x  , y+1, QUESTION_COIN[2])
                pyxel.tilemaps[0].pset(x+1, y+1, QUESTION_COIN[3])
            if self.map[x][y] == HIDDEN_COIN[0] or self.map[x][y] == HIDDEN_MUSHROOM[0]:
                pyxel.tilemaps[0].pset(x  , y  , (0, 0))
                pyxel.tilemaps[0].pset(x+1, y  , (0, 0))
                pyxel.tilemaps[0].pset(x  , y+1, (0, 0))
                pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
            if self.map[x][y] == MAP_COIN[0]:
                pyxel.tilemaps[0].pset(x  , y  , MAP_COIN[0])
                pyxel.tilemaps[0].pset(x+1, y  , MAP_COIN[1])
                pyxel.tilemaps[0].pset(x  , y+1, MAP_COIN[2])
                pyxel.tilemaps[0].pset(x+1, y+1, MAP_COIN[3])

    def getcoin(self):
        pyxel.play(3, 0) # Coin Sound
        self.coins += 1
        if self.coins >= 100:
            pyxel.play(3, 3) # 1-Up Mushroom Sound
            self.coins -= 100
            self.lives += 1
        self.score += 100

    def setdemomap(self):
        self.demostage = random.randrange(MAX_STAGE-1)
        self.demomap_x  = STAGE_MAP[self.demostage][0]*256
        self.demomap_y8 = STAGE_MAP[self.demostage][1]*32
        self.demowait = 200

    def update(self):
        if self.status == STATUS_TITLE:
            if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_S) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_X):
                if not (pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y)):
                    self.stage = self.stagemap = START_STAGEMAP
                self.status = STATUS_OPENING
                self.score = 0
                self.coins = 0
                self.lives = 3
                self.remaintime = START_TIME
                return
            if self.demowait:
                self.demowait -= 1
                return
            if self.demomap_x >= 256*7:
                self.setdemomap()
                return
            self.demomap_x += 1
            if self.demomap_x >= 256*7:
                self.demowait = 100
            return
        if self.status == STATUS_OPENING:
            if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_Z) or \
                    pyxel.btnr(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B):
                self.status = STATUS_PLAY
                self.remaintime = START_TIME
                self.stagemap = self.stage
                self.start()
            return
        if self.status == STATUS_ENDING or self.status == STATUS_GAMEOVER:
            if pyxel.play_pos(0) == None:
                self.status = STATUS_TITLE
                self.setdemomap()
            return
        if self.status == STATUS_PAUSE:
            if pyxel.btnr(pyxel.KEY_S) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_X):
                self.status = STATUS_PLAY
            return
        if not self.istimestop:
            self.remaintime -= 1
            if self.remaintime <= 0:
                self.isgameover = WAITTIME

        # Game Over
        if self.isgameover > 1:
            if self.isgameover == WAITTIME:
                pyxel.stop()
                pyxel.playm(1, loop=False) # Death Sound
            self.isgameover -= 1
            self.dy = -12
            self.istimestop = 1
            return
        if self.isgameover == 1:
            self.dy += 1
            self.player_y += self.dy
            if self.player_y > 256+16*2:
                self.isgameover = -1
            return
        if self.isgameover == -1:
            if pyxel.play_pos(0) == None:
                self.issupermario = 0
                self.lives -= 1
                if self.lives <= 0:
                    pyxel.playm(2, loop=False) # Game Over Sound
                    self.status = STATUS_GAMEOVER
                else:
                    self.status = STATUS_OPENING
            return

        # Goal
        if self.isgoal == GOAL_BEGIN:
            pyxel.stop()
            if self.isrescue:
                pyxel.play(1, 28) # Rescue Fanfare
                self.score += 10000
            else:
                pyxel.play(1, 29) # Flagpole Fanfare
                self.score += (64-self.player_y//4)*100
            self.score += (self.remaintime//30)*20
            self.isgoal = GOAL_STOP
            self.istimestop = 1
            return
        if self.isgoal == GOAL_STOP:
            if pyxel.play_pos(1) == None:
                if not self.isrescue or pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_Z) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B):
                    self.isgoal = GOAL_JUMP
            return
        if self.isgoal == GOAL_JUMP:
            self.dy -= 1
            self.player_y += self.dy
            for i in range(len(self.rescue)):
                if self.rescue[i].alive:
                    self.rescue[i].curt_y += self.dy
            if self.player_y < -16*2:
                if self.stage >= MAX_STAGE-1:
                    if self.round == MAX_ROUND-1:
                        pyxel.playm(2, loop=False) # Game Over Sound
                        self.status = STATUS_ENDING
                        return
                    self.roundup()
                self.stage = STAGE_MAP[self.stagemap][5]
                self.status = STATUS_OPENING
            return

        # Warp
        if self.iswarp > 1:
            if self.iswarp == WAITTIME:
                pyxel.play(3, 22) # Damage/Warp Sound
            self.iswarp -= 1
            return
        elif self.iswarp == 1:
            self.stagemap = STAGE_MAP[self.stagemap][6][self.nextstagemap]
            self.start()
            return

        if pyxel.play_pos(0) == None:
            pyxel.playm(0, loop=True)

        # Invulnerable
        if self.isinvulnerable > 0:
            self.isinvulnerable -= 1

        # Kuribo
        for i in range(len(self.kuribo)):
            ret = self.kuribo[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy, \
                    self.brick, self.question)
            if ret == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME
            elif ret == RET_STOMPED:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.score += 100
                self.dy = -8

        # Togezo
        for i in range(len(self.togezo)):
            if self.togezo[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy, \
                    self.brick, self.question) == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME

        # Kuppa
        for i in range(len(self.kuppa)):
            if self.kuppa[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy, \
                    self.brick, self.question, self.firebreath) == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME

        # FireBreath
        for i in reversed(range(len(self.firebreath))):
            ret = self.firebreath[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy)
            if ret == RET_SCREENOUT:
                del self.firebreath[i]
            elif ret == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME

        # RandomKiller
        if random.randrange(40) == 0 and len(self.randomkiller) < self.round*2:
            self.randomkiller.append(RandomKiller(self.map_x))
        for i in reversed(range(len(self.randomkiller))):
            ret = self.randomkiller[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy)
            if ret == RET_SCREENOUT:
                del self.randomkiller[i]
            elif ret == RET_STOMPED:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.score += 200
                self.dy = -8
            elif ret == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME

        # HodaiKiller
        for i in range(len(self.hodaikiller)):
            ret = self.hodaikiller[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy)
            if ret == RET_STOMPED:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.score += 200
                self.dy = -8
            elif ret == RET_ATTACK and not self.isinvulnerable:
                if self.issupermario:
                    pyxel.play(3, 22) # Damage/Warp Sound
                    self.issupermario = 0
                    self.isinvulnerable = INVULNERABLETIME
                else:
                    self.isgameover = WAITTIME

        # Brick
        for i in reversed(range(len(self.brick))):
            if self.brick[i].update():
                c = self.map[self.brick[i].init_x//8][self.brick[i].init_y//8]
                if c == BRICK_MUSHROOM[0] or c == HIDDEN_MUSHROOM[0]:
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8  , EMPTY_BLOCK[0])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8  , EMPTY_BLOCK[1])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8+1, EMPTY_BLOCK[2])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8+1, EMPTY_BLOCK[3])
                    self.mushroom = Mushroom(self.brick[i].init_x, self.brick[i].init_y-16)
                elif c == BRICK_COIN[0] or c == HIDDEN_COIN[0]:
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8  , EMPTY_BLOCK[0])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8  , EMPTY_BLOCK[1])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8+1, EMPTY_BLOCK[2])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8+1, EMPTY_BLOCK[3])
                    self.blockcoin = BlockCoin(self.brick[i].init_x, self.brick[i].init_y-16)
                elif self.brick[i].item != ITEM_BREAK:
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8  , BRICK_NORMAL[0])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8  , BRICK_NORMAL[0])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8  , self.brick[i].init_y//8+1, BRICK_NORMAL[1])
                    pyxel.tilemaps[0].pset(self.brick[i].init_x//8+1, self.brick[i].init_y//8+1, BRICK_NORMAL[1])
                del self.brick[i]

        # Question
        for i in reversed(range(len(self.question))):
            if self.question[i].update():
                pyxel.tilemaps[0].pset(self.question[i].init_x//8  , self.question[i].init_y//8  , EMPTY_BLOCK[0])
                pyxel.tilemaps[0].pset(self.question[i].init_x//8+1, self.question[i].init_y//8  , EMPTY_BLOCK[1])
                pyxel.tilemaps[0].pset(self.question[i].init_x//8  , self.question[i].init_y//8+1, EMPTY_BLOCK[2])
                pyxel.tilemaps[0].pset(self.question[i].init_x//8+1, self.question[i].init_y//8+1, EMPTY_BLOCK[3])
                if self.map[self.question[i].init_x//8][self.question[i].init_y//8] == QUESTION_MUSHROOM[0]:
                    self.mushroom = Mushroom(self.question[i].init_x, self.question[i].init_y-16)
                else:
                    self.blockcoin = BlockCoin(self.question[i].init_x, self.question[i].init_y-16)
                del self.question[i]

        # Mushroom
        if self.mushroom:
            ret = self.mushroom.update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy, self.brick, self.question)
            if ret == RET_SCREENOUT:
                self.mushroom = None
            elif ret == RET_TOUCH:
                pyxel.play(3, 4) # Power-Up Sound
                self.score += 1000
                self.mushroom = None
                self.issupermario = 1

        # BlockCoin
        if self.blockcoin:
            if self.blockcoin.update() == RET_SCREENOUT:
                self.blockcoin = None

        # Player
        if self.isjump: # Jump or Fall
            self.dy += 1
            if not(pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)):
                if self.dy < -1:
                    self.dy += 2
            if self.dy > 7:
                self.dy = 7
            self.player_y += self.dy
            if self.player_y >= 16*16: # Bottomless Fall
                self.isgameover = WAITTIME
            up1  = self.gettilemap(self.player_x+self.map_x+ 2, self.player_y)
            up2  = self.gettilemap(self.player_x+self.map_x+13, self.player_y)
            upm1 = self.getmap(self.player_x+self.map_x+2 , self.player_y)
            upm2 = self.getmap(self.player_x+self.map_x+13, self.player_y)
            if self.dy < 0 and (up1 in NOMOVE or up2 in NOMOVE or upm1 in HIDDEN_ALL or upm2 in HIDDEN_ALL): # ceiling
                if ((up1 in BRICK_NORMAL or (up1==(0, 0) and upm1 in HIDDEN_ALL)) \
                        and (up2 in BRICK_NORMAL or (up2==(0, 0) and upm2 in HIDDEN_ALL)) \
                        and (self.player_x+self.map_x+2)%16 < 10) \
                        or ((up1 in BRICK_NORMAL or (up1==(0, 0) and upm1 in HIDDEN_ALL)) and \
                        not(up2 in BRICK_NORMAL or (up2==(0, 0) and upm2 in HIDDEN_ALL))): # Left-Brick
                    x = (self.player_x+self.map_x+ 2)//16*2
                    y = (self.map_y8*8+self.player_y)//16*2
                    pyxel.tilemaps[0].pset(x,   y  , (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y  , (1, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (1, 0))
                    if upm1 in BRICK_COIN or upm1 in HIDDEN_COIN:
                        self.getcoin()
                        self.brick.append(Brick(x*8, y*8, ITEM_COIN))
                    elif upm1 in BRICK_MUSHROOM or upm1 in HIDDEN_MUSHROOM:
                        pyxel.play(3, 27) # Item Block Sound
                        self.brick.append(Brick(x*8, y*8, ITEM_MUSHROOM))
                    elif self.issupermario:
                        pyxel.tilemaps[0].pset(x,   y  , (0, 0))
                        pyxel.tilemaps[0].pset(x+1, y  , (0, 0))
                        pyxel.tilemaps[0].pset(x,   y+1, (0, 0))
                        pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
                        self.score += 50
                        self.brick.append(Brick(x*8, y*8, ITEM_BREAK))
                    else:
                        self.brick.append(Brick(x*8, y*8, ITEM_EMPTY))
                elif up2 in BRICK_NORMAL or (up2==(0, 0) and upm2 in HIDDEN_ALL): # Right-Brick
                    x = (self.player_x+self.map_x+13)//16*2
                    y = (self.map_y8*8+self.player_y)//16*2
                    pyxel.tilemaps[0].pset(x,   y  , (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y  , (1, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (1, 0))
                    if upm2 in BRICK_COIN or upm2 in HIDDEN_COIN:
                        self.getcoin()
                        self.brick.append(Brick(x*8, y*8, ITEM_COIN))
                    elif upm2 in BRICK_MUSHROOM or upm2 in HIDDEN_MUSHROOM:
                        pyxel.play(3, 27) # Item Block Sound
                        self.brick.append(Brick(x*8, y*8, ITEM_MUSHROOM))
                    elif self.issupermario:
                        pyxel.tilemaps[0].pset(x,   y  , (0, 0))
                        pyxel.tilemaps[0].pset(x+1, y  , (0, 0))
                        pyxel.tilemaps[0].pset(x,   y+1, (0, 0))
                        pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
                        self.score += 50
                        self.brick.append(Brick(x*8, y*8, ITEM_BREAK))
                    else:
                        self.brick.append(Brick(x*8, y*8, ITEM_EMPTY))
                elif (up1 in QUESTION_COIN and up2 in QUESTION_COIN and (self.player_x+self.map_x+2)%16 < 10) \
                        or (up1 in QUESTION_COIN and not up2 in QUESTION_COIN): # ?-Block
                    x = (self.player_x+self.map_x+ 2)//16*2
                    y = (self.map_y8*8+self.player_y)//16*2
                    pyxel.tilemaps[0].pset(x,   y  , (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y  , (1, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (1, 0))
                    if upm1 in QUESTION_COIN:
                        self.getcoin()
                    elif upm1 in QUESTION_MUSHROOM:
                        pyxel.play(3, 27) # Item Block Sound
                    self.question.append(Question(x*8, y*8))
                elif up2 in QUESTION_COIN:
                    x = (self.player_x+self.map_x+13)//16*2
                    y = (self.map_y8*8+self.player_y)//16*2
                    pyxel.tilemaps[0].pset(x,   y  , (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y  , (1, 0))
                    pyxel.tilemaps[0].pset(x,   y+1, (1, 0))
                    pyxel.tilemaps[0].pset(x+1, y+1, (1, 0))
                    if upm2 in QUESTION_COIN:
                        self.getcoin()
                    elif upm2 in QUESTION_MUSHROOM:
                        pyxel.play(3, 27) # Item Block Sound
                    self.question.append(Question(x*8, y*8))
                
                self.player_y = self.player_y+16-(self.player_y%16)
                self.dy = 0
            down1 = self.gettilemap(self.player_x+self.map_x+ 2, self.player_y+16)
            down2 = self.gettilemap(self.player_x+self.map_x+13, self.player_y+16)
            if self.dy >= 0 and (down1 in NOMOVE or down2 in NOMOVE): # Landing
                self.dy = 0
                self.isjump = 0
                self.player_y = self.player_y - (self.player_y%16)
        else:
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
                if not self.isjumpkey:
                    pyxel.play(2, 1) # Jump Sound
                    self.isjump = 1
                    if self.dx == 4 or self.dx == -4: # X(Y)-Buttom-Jump
                        self.player_y -= 2
                        self.dy = -13
                    else:
                        self.dy = -12
                    remain = (self.player_x+self.map_x)%16
                    if self.dx == 0 and 3 <= remain <= 5:
                        self.player_x -= remain-2
                    if self.dx == 0 and 10 <= remain <= 12:
                        self.player_x += 16-remain-2
                self.isjumpkey = 1
            else:
                self.isjumpkey = 0
            if not self.isjump:
                down1 = self.gettilemap(self.player_x+self.map_x+ 2, self.player_y+16)
                down2 = self.gettilemap(self.player_x+self.map_x+13, self.player_y+16)
                if (not down1 in NOMOVE) and (not down2 in NOMOVE): # 床なし
                    self.isjump = 1
                    self.isrun = 0
                    self.dy = -1

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dirct = 1
            self.dx += 1
            if pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y):
                if self.dx > 4:
                    self.dx = 4
            else:
                if self.dx > 3:
                    self.dx = 3
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dirct = -1
            self.dx -= 1
            if pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y):
                if self.dx < -4:
                    self.dx = -4
            else:
                if self.dx < -3:
                    self.dx = -3
        else:
            if self.dx > 0:
                self.dx -= 1
            elif self.dx < 0:
                self.dx += 1

        if self.player_x+self.map_x+self.dx > 256*7+16*15:
            self.dx = (256*7+16*15)-(self.player_x+self.map_x)
        if self.player_x+self.dx < 0:
            self.dx = -self.player_x

        if self.dx > 0:
            right1 = self.gettilemap(self.player_x+self.map_x+self.dx+15, self.player_y   )
            right2 = self.gettilemap(self.player_x+self.map_x+self.dx+15, self.player_y+15)
            if right1 in NOMOVE or right2 in NOMOVE:
                pass
            else:
                if self.map_x == 256*7 or self.player_x < 16*(15-OUTLOOK):
                    self.player_x += self.dx
                else:
                    if self.map_x//16 != (self.map_x+self.dx)//16:
                        for i in range(len(self.kuribo)):
                            if self.kuribo[i].alive == 0 and self.kuribo[i].init_y//256 == self.map_y8//32 and \
                                    self.kuribo[i].init_x//16 == (self.map_x+self.dx)//16+17:
                                self.kuribo[i].alive = 1
                                self.kuribo[i].dx = -1
                        for i in range(len(self.togezo)):
                            if self.togezo[i].alive == 0 and self.togezo[i].init_y//256 == self.map_y8//32 and \
                                    self.togezo[i].init_x//16 == (self.map_x+self.dx)//16+17:
                                self.togezo[i].alive = 1
                                self.togezo[i].dx = -1
                        for i in range(len(self.kuppa)):
                            if self.kuppa[i].alive == 0 and self.kuppa[i].init_y//256 == self.map_y8//32 and \
                                    self.kuppa[i].init_x//16 == (self.map_x+self.dx)//16+17:
                                self.kuppa[i].alive = 1
                                self.kuppa[i].dx = -1
                        for i in range(len(self.rescue)):
                            if self.rescue[i].alive == 0 and self.rescue[i].init_y//256 == self.map_y8//32 and \
                                    self.rescue[i].init_x//16 == (self.map_x+self.dx)//16+17:
                                self.rescue[i].alive = 1
                        for i in range(16):
                            x = ((self.map_x+self.dx)//16+17)*2
                            y = (self.map_y8//32*16+i)*2
                            self.sethiddenitem(x, y)

                    self.map_x += self.dx
                    if self.map_x > 256*7:
                        self.player_x += self.map_x-256*7
                        self.map_x = 256*7
                if self.player_x < 0:
                    self.player_x = 0
                if self.player_x > 16*15:
                    self.player_x = 16*15
                self.runptn = self.runptn + 1
                if self.runptn > 3:
                    self.runptn = 0
                self.isrun = 1
        elif self.dx < 0:
            left1 = self.gettilemap(self.player_x+self.map_x+self.dx, self.player_y   )
            left2 = self.gettilemap(self.player_x+self.map_x+self.dx, self.player_y+15)
            if left1 in NOMOVE or left2 in NOMOVE:
                pass
            else:
                if self.map_x == 0 or self.player_x > 16*OUTLOOK:
                    self.player_x += self.dx
                else:
                    if self.map_x//16 != (self.map_x+self.dx)//16:
                        for i in range(len(self.kuribo)):
                            if self.kuribo[i].alive == 0 and \
                                    self.kuribo[i].init_y//256 == self.map_y8//32 and \
                                    self.kuribo[i].init_x//16 == (self.map_x+self.dx)//16-1:
                                self.kuribo[i].alive = 1
                                self.kuribo[i].dx = 1
                        for i in range(len(self.togezo)):
                            if self.togezo[i].alive == 0 and \
                                    self.togezo[i].init_y//256 == self.map_y8//32 and \
                                    self.togezo[i].init_x//16 == (self.map_x+self.dx)//16-1:
                                self.togezo[i].alive = 1
                                self.togezo[i].dx = 1
                        for i in range(len(self.kuppa)):
                            if self.kuppa[i].alive == 0 and \
                                    self.kuppa[i].init_y//256 == self.map_y8//32 and \
                                    self.kuppa[i].init_x//16 == (self.map_x+self.dx)//16-1:
                                self.kuppa[i].alive = 1
                                self.kuppa[i].dx = 1
                        for i in range(16):
                            x = ((self.map_x+self.dx)//16-1)*2
                            y = (self.map_y8//32*16+i)*2
                            self.sethiddenitem(x, y)

                    self.map_x += self.dx
                    if self.map_x < 0:
                        self.player_x += self.map_x
                        self.map_x = 0
                if self.player_x < 0:
                    self.player_x = 0
                if self.player_x > 16*15:
                    self.player_x = 16*15
                self.runptn = self.runptn + 1
                if self.runptn > 3:
                    self.runptn = 0
                self.isrun = -1
        if self.dx == 0:
            self.isrun = 0

        # MapCoin
        center = self.gettilemap(self.player_x+self.map_x+7, self.player_y+7)
        if center in MAP_COIN:
            x = (self.map_x   +self.player_x+7)//16*2
            y = (self.map_y8*8+self.player_y+7)//16*2
            pyxel.tilemaps[0].pset(x  , y  , (0, 0))
            pyxel.tilemaps[0].pset(x+1, y  , (0, 0))
            pyxel.tilemaps[0].pset(x  , y+1, (0, 0))
            pyxel.tilemaps[0].pset(x+1, y+1, (0, 0))
            self.getcoin()

        # Goal
        if center in GOAL:
            self.isgoal = GOAL_BEGIN
            self.isrescue = 0

        # Rescue
        for i in range(len(self.rescue)):
            if self.rescue[i].update(self.map_x, self.map_y8, self.player_x, self.player_y, self.dy) == RET_TOUCH:
                self.isgoal = GOAL_BEGIN
                self.isrescue = 1

        # WarpPipe
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            downm = self.getmap(self.player_x+self.map_x+3, self.player_y+16)
            if downm in (WARPPIPE[0], WARPPIPE[2]):
                self.nextstagemap = self.warp_xy.index([(self.player_x+self.map_x+3)//8, self.map_y8+(self.player_y+16)//8])
                self.iswarp = WAITTIME

        if pyxel.btnr(pyxel.KEY_S) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_X):
            pyxel.stop()
            pyxel.play(1, 34) # Pause Sound
            self.status = STATUS_PAUSE
        return

    def printstatus(self):
        pyxel.rect(0, 0, 256, Y_SHIFT, pyxel.COLOR_BLACK)
        col = pyxel.COLOR_WHITE
        if self.round == 1:
            col = pyxel.COLOR_YELLOW
        elif self.round > 1:
            col = pyxel.COLOR_RED
        pyxel.text(4, 4, f'SCORE:{self.score:7}   COIN:{self.coins:3}   MARIO:{self.lives:2}   STAGE:{self.stage+1:2}   TIME:{self.remaintime//30:4}', col)

    def printtext(self, x, y, text):
        for i in range(3):
            for j in range(3):
                pyxel.text(x+j, y+i, text, pyxel.COLOR_BLACK)
        pyxel.text(x+1, y+1, text, pyxel.COLOR_WHITE)

    def draw(self):
        if self.status == STATUS_TITLE:
            pyxel.cls(STAGE_MAP[self.demostage][4])
            self.printstatus()
            pyxel.bltm(0, Y_SHIFT, 0, self.demomap_x, self.demomap_y8*8, 256, 256, 6)
            pyxel.blt(16*5+8, 16*6+4, 0, 16*0, 16*8, 16*5, 16*2, 6)
            self.printtext(95, 144, 'PUSH SPACE-KEY OR')
            self.printtext(89, 154, 'GAMEPAD-START-BUTTON')
        elif self.status == STATUS_OPENING:
            pyxel.cls(pyxel.COLOR_BLACK)
            self.printstatus()
            self.printtext(114, 99, f'STAGE {self.stage+1}')
            pyxel.blt(112, 120, 0, 16, 0, 16, 16, 6)  # Mario
            self.printtext(131, 125, f'x {self.lives}')
        elif self.status == STATUS_ENDING:
            pyxel.cls(pyxel.COLOR_BLACK)
            self.printstatus()
            self.printtext(114, 99, 'GAME CLEAR')
            pyxel.blt(106, 125, 0,  16,  0, 16, 16, 6) # Mario
            pyxel.blt(126, 117, 0, 192, 40, 16, 24, 6) # Peach
            pyxel.blt(146, 117, 0, 208, 40, 16, 24, 6) # Pinokio
        elif self.status == STATUS_GAMEOVER:
            pyxel.cls(pyxel.COLOR_BLACK)
            self.printstatus()
            self.printtext(114, 99, 'GAME OVER')
        else:
            pyxel.cls(STAGE_MAP[self.stagemap][4])
            pyxel.rect(0, 0, 256, Y_SHIFT, pyxel.COLOR_BLACK)
            self.printstatus()
            pyxel.bltm(0, Y_SHIFT, 0, self.map_x, self.map_y8*8, 256, 256, 6)

            for i in range(len(self.kuribo)): # Kuribo
                if self.kuribo[i].isstomp:
                    pyxel.blt(self.kuribo[i].curt_x-self.map_x, self.kuribo[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*5, 16*2, 16, 16, 6)
                elif self.kuribo[i].isbounce:
                    pyxel.blt(self.kuribo[i].curt_x-self.map_x, self.kuribo[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*4, 16*2, 16, -16, 6)
                elif self.kuribo[i].alive:
                    pyxel.blt(self.kuribo[i].curt_x-self.map_x, self.kuribo[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*4, 16*2, 16 if self.kuribo[i].ptn//5%2 else -16, 16, 6)

            for i in range(len(self.togezo)): # Togezo
                if self.togezo[i].isbounce:
                    pyxel.blt(self.togezo[i].curt_x-self.map_x, self.togezo[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*2 if self.togezo[i].ptn//5%2 else 16*3, 16*2, 16 if self.togezo[i].dx<0 else -16, -16, 6)
                elif self.togezo[i].alive:
                    pyxel.blt(self.togezo[i].curt_x-self.map_x, self.togezo[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*2 if self.togezo[i].ptn//5%2 else 16*3, 16*2, 16 if self.togezo[i].dx<0 else -16, 16, 6)

            for i in range(len(self.kuppa)): # Kuppa
                if self.kuppa[i].isbreath:
                    pyxel.blt(self.kuppa[i].curt_x-self.map_x, self.kuppa[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*10, 16*2, -32*self.kuppa[i].dirct, 32, 6)
                elif self.kuppa[i].alive:
                    pyxel.blt(self.kuppa[i].curt_x-self.map_x, self.kuppa[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*6 if self.kuppa[i].ptn//15%2 else 16*8, 16*2, -32*self.kuppa[i].dirct, 32, 6)

            for i in range(len(self.firebreath)): # FireBreath
                pyxel.blt(self.firebreath[i].curt_x-self.map_x, self.firebreath[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                        16*12, 16*2, -24*self.firebreath[i].dx, 8, 6)

            for i in range(len(self.randomkiller)): # RandomKiller
                pyxel.blt(self.randomkiller[i].curt_x-self.map_x, self.randomkiller[i].curt_y+Y_SHIFT, 0, \
                        16*1, 16*2, -16*self.randomkiller[i].dirct, 16, 6)

            for i in range(len(self.hodaikiller)): # HodaiKiller
                if self.hodaikiller[i].alive:
                    pyxel.blt(self.hodaikiller[i].curt_x-self.map_x, self.hodaikiller[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                            16*1, 16*2, -16*self.hodaikiller[i].dirct, 16, 6)

            for i in range(len(self.brick)): # Brick break
                if self.brick[i].item == ITEM_BREAK:
                    pyxel.blt(self.brick[i].x1-self.map_x, self.brick[i].y1-self.map_y8*8+Y_SHIFT, 0, 8*24, 8*2, 8, 8, 6)
                    pyxel.blt(self.brick[i].x2-self.map_x, self.brick[i].y2-self.map_y8*8+Y_SHIFT, 0, 8*25, 8*2, 8, 8, 6)
                    pyxel.blt(self.brick[i].x3-self.map_x, self.brick[i].y3-self.map_y8*8+Y_SHIFT, 0, 8*24, 8*3, 8, 8, 6)
                    pyxel.blt(self.brick[i].x4-self.map_x, self.brick[i].y4-self.map_y8*8+Y_SHIFT, 0, 8*25, 8*3, 8, 8, 6)
                else:
                    pyxel.blt(self.brick[i].x-self.map_x  , self.brick[i].y-self.map_y8*8+Y_SHIFT, 0, 16, 16, 8, 16, 6)
                    pyxel.blt(self.brick[i].x-self.map_x+8, self.brick[i].y-self.map_y8*8+Y_SHIFT, 0, 16, 16, 8, 16, 6)

            for i in range(len(self.question)): # Question break / Empty
                pyxel.blt(self.question[i].x-self.map_x, self.question[i].y-self.map_y8*8+Y_SHIFT, 0, 16*3, 16, 16, 16, 6)

            if self.mushroom: # Mushroom
                pyxel.blt(self.mushroom.curt_x-self.map_x, self.mushroom.curt_y-self.map_y8*8+Y_SHIFT+16-self.mushroom.count, 0, \
                        16*1, 16*4, 16, self.mushroom.count, 6)

            if self.blockcoin: # BlockCoin
                pyxel.blt(self.blockcoin.curt_x-self.map_x, self.blockcoin.curt_y-self.map_y8*8+Y_SHIFT, 0, \
                        16*0, 16*4, 16, 16, 6)

            for i in range(len(self.rescue)): # Rescue
                if self.rescue[i].alive:
                    if self.stage == MAX_STAGE-1 and self.round == MAX_ROUND-1: # Peach
                        if self.isrescue:
                            self.printtext(self.rescue[i].init_x-self.map_x-33, self.rescue[i].init_y-self.map_y8*8+Y_SHIFT-71, \
                                    'THANK YOU MARIO!')
                            self.printtext(self.rescue[i].init_x-self.map_x-37, self.rescue[i].init_y-self.map_y8*8+Y_SHIFT-53, \
                                    'YOUR QUEST IS OVER.')
                        pyxel.blt(self.rescue[i].curt_x-self.map_x, self.rescue[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                                16*12, 8*5, 16, 24, 6)
                    else: # Kinopio
                        if self.isrescue:
                            self.printtext(self.rescue[i].init_x-self.map_x-33, self.rescue[i].init_y-self.map_y8*8+Y_SHIFT-71, \
                                    'THANK YOU MARIO!')
                            self.printtext(self.rescue[i].init_x-self.map_x-45, self.rescue[i].init_y-self.map_y8*8+Y_SHIFT-53, \
                                    'BUT OUR PRINCESS IS IN')
                            self.printtext(self.rescue[i].init_x-self.map_x-45, self.rescue[i].init_y-self.map_y8*8+Y_SHIFT-41, \
                                    'ANOTHER PLACE!')
                        pyxel.blt(self.rescue[i].curt_x-self.map_x, self.rescue[i].curt_y-self.map_y8*8+Y_SHIFT, 0, \
                                16*13, 8*5, 16, 24, 6)

            if self.isgoal == GOAL_JUMP: # Goal
                pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, 16*CHARA_JUMP, self.issupermario*16*5, 16*self.dirct, 16, 6)
            elif self.isgameover: # GameOver
                pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, 16*CHARA_GAMEOVER, self.issupermario*16*5, 16, 16, 6)
                if self.remaintime <= 0:
                    self.printtext(118, 99, 'TIME UP')
            elif self.iswarp: # Warp
                if self.iswarp > WAITTIME-16:
                    pyxel.blt(self.player_x, self.player_y+Y_SHIFT+WAITTIME-self.iswarp, 0, \
                            16, self.issupermario*16*5, 16, 16-(WAITTIME-self.iswarp), 6)
            else: # Mario
                if (self.isinvulnerable % 4) == 3: # Invulnerable Blink
                    pass
                else:
                    if self.isjump:
                        pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, \
                                16*CHARA_JUMP, self.issupermario*16*5, 16*self.dirct, 16, 6)
                    elif self.isrun:
                        if self.isrun == self.dirct:
                            pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, 
                                    CHARA_RUN[self.runptn]*16, self.issupermario*16*5, 16*self.dirct, 16, 6)
                        else:
                            pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, 
                                    16*CHARA_BRAKE, self.issupermario*16*5, 16*self.dirct, 16, 6)
                    else:
                        pyxel.blt(self.player_x, self.player_y+Y_SHIFT, 0, 16, self.issupermario*16*5, 16*self.dirct, 16, 6)

            if self.status == STATUS_PAUSE:
                self.printtext(119, 99, 'PAUSE')

class Brick:
    def __init__(self, x, y, item):
        self.init_x = x
        self.init_y = y
        self.item = item
        self.isbounce = 2
        if item == ITEM_BREAK:
            self.x1 = self.x3 = x     -8
            self.x2 = self.x4 = x+8   +8
            self.y1 = self.y2 = y  -16-8
            self.y3 = self.y4 = y+8-16+8
            self.count = 16
            self.dx = 2
            self.dy = -4
        else:
            self.x = x
            self.y = y
            self.dy = -4

    def update(self):
        if self.isbounce:
            self.isbounce -= 1
        if self.item == ITEM_BREAK:
            self.count -= 1
            if self.count < 0:
                return True
            self.dy += 1
            self.x1 -= self.dx
            self.x2 += self.dx
            self.x3 -= self.dx
            self.x4 += self.dx
            self.y1 += self.dy
            self.y2 += self.dy
            self.y3 += self.dy+2
            self.y4 += self.dy+2
            return False
        else:
            self.dy += 1
            self.y += self.dy
            if self.y >= self.init_y:
                self.y = self.init_y
                return True
            return False

class Question:
    def __init__(self, x, y):
        self.init_x = self.x = x
        self.init_y = self.y = y
        self.dy = -4
        self.isbounce = 2

    def update(self):
        if self.isbounce:
            self.isbounce -= 1
        self.dy += 1
        self.y += self.dy
        if self.y >= self.init_y:
            self.y = self.init_y
            return True
        return False

class Mushroom:
    def __init__(self, x, y):
        self.init_x = self.curt_x = x
        self.init_y = self.curt_y = y
        self.dx = 2
        self.dy = 0
        self.count = 0

    def gettilemap(self, x, y, map_y8):
        if x < 0 or x >= 256*8 or y < map_y8*8 or y >=  map_y8*8+256:
            return -1
        return pyxel.tilemaps[0].pget(x//8, y//8)

    def update(self, map_x, map_y8, player_x, player_y, player_dy, brick, question):
        if self.count < 16:
            self.count += 2
            if self.count > 16:
                self.count = 16
        else:
            if self.curt_x-16+3 < player_x+map_x < self.curt_x+16-3 \
                    and self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+16-3: # Player接触
                return RET_TOUCH

            self.curt_x += self.dx
            if self.curt_x < map_x-16*3 or self.curt_x > map_x+256+16*2: # 左右スクリーンアウト
                return RET_SCREENOUT

            self.curt_y += self.dy
            if self.curt_y-map_y8*8 >= 16*16: # 下スクリーンアウト
                return RET_SCREENOUT

            for i in range(len(brick)): # 下から叩かれたレンガ
                if brick[i].isbounce and self.curt_x-16+3 < brick[i].init_x < self.curt_x+16-3 \
                        and self.curt_y-16+3 < brick[i].init_y-16 < self.curt_y+16-3:
                    if self.curt_x-16+3 < brick[i].init_x < self.curt_x:
                        self.dx = 2
                    else:
                        self.dx = -2
                    self.dy = -6
                    return RET_BOUNCE

            for i in range(len(question)): # 下から叩かれたブロック
                if question[i].isbounce and self.curt_x-16+3 < question[i].init_x < self.curt_x+16-3 \
                        and self.curt_y-16+3 < question[i].init_y-16 < self.curt_y+16-3:
                    if self.curt_x-16+3 < question[i].init_x < self.curt_x:
                        self.dx = 2
                    else:
                        self.dx = -2
                    self.dy = -6
                    return RET_BOUNCE

            down1 = self.gettilemap(self.curt_x+ 2, self.curt_y+16, map_y8)
            down2 = self.gettilemap(self.curt_x+13, self.curt_y+16, map_y8)
            if down1 in NOMOVE or down2 in NOMOVE: # 床あり
                self.dy = 0
                self.curt_y = self.curt_y - (self.curt_y%16)
            else:
                self.dy += 1
                if self.dy > 7:
                    self.dy = 7

            if self.dx < 0:
                map1 = self.gettilemap(self.curt_x, self.curt_y   , map_y8)
                map2 = self.gettilemap(self.curt_x, self.curt_y+15, map_y8)
            else:
                map1 = self.gettilemap(self.curt_x+15, self.curt_y   , map_y8)
                map2 = self.gettilemap(self.curt_x+15, self.curt_y+15, map_y8)
            if map1 in NOMOVE or map2 in NOMOVE: # 壁あり
                self.dx *= -1
                self.curt_x += self.dx
            return RET_NONE

class BlockCoin:
    def __init__(self, x, y):
        self.curt_x = x
        self.curt_y = y
        self.dy = -6
        self.count = 13

    def update(self):
        self.curt_y += self.dy
        self.dy += 1
        if self.dy > 7:
            self.dy = 7
        self.count -= 1
        if self.count < 0:
            return RET_SCREENOUT
        return RET_NONE

class Kuribo:
    def __init__(self, x, y):
        self.init_x = self.curt_x = x
        self.init_y = self.curt_y = y
        self.dx = 0
        self.dy = 0
        self.ptn = 0
        self.alive = 0
        self.isstomp = 0
        self.isbounce = 0

    def reset(self):
        self.curt_x = self.init_x
        self.curt_y = self.init_y
        self.dx = 0
        self.dy = 0
        self.ptn = 0
        self.alive = 0
        self.isstomp = 0
        self.isbounce = 0

    def gettilemap(self, x, y, map_y8):
        if x < 0 or x >= 256*8 or y < map_y8*8 or y >=  map_y8*8+256:
            return -1
        return pyxel.tilemaps[0].pget(x//8, y//8)

    def attack(self, player_dy):
        if player_dy > 0: # 踏みつけ
            self.isstomp = 5
            return RET_STOMPED
        else:
            return RET_ATTACK

    def update(self, map_x, map_y8, player_x, player_y, player_dy, brick, question):
        if self.isstomp:
            self.isstomp -= 1
            if self.isstomp == 0:
                self.reset()
            return RET_NONE

        if self.isbounce: # 下からレンガで叩かれる
            self.dy += 1
            self.curt_y += self.dy
            self.curt_x += self.dx
            self.isbounce -= 1 # 所定の回数で消える
            if self.isbounce == 0:
                self.reset()
            return RET_NONE

        if not self.alive:
            return RET_NONE

        self.ptn += 1

        self.curt_x += self.dx
        if self.curt_x < map_x-16*2 or self.curt_x > map_x+256+16: # スクリーンアウト
            self.reset()
            return RET_SCREENOUT

        self.curt_y += self.dy
        if self.curt_y-map_y8*8 >= 16*16:
            self.reset()
            return RET_SCREENOUT

        if self.curt_x-16+3 < player_x+map_x < self.curt_x+16-3 \
                and self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+16-3:
            return self.attack(player_dy)

        for i in range(len(brick)):
            if self.curt_x-16+3 < brick[i].init_x < self.curt_x+16-3 \
                    and self.curt_y-16+3 < brick[i].init_y-16 < self.curt_y+16-3:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.isbounce = 20
                self.dy = -6
                return RET_BOUNCE

        for i in range(len(question)):
            if self.curt_x-16+3 < question[i].init_x < self.curt_x+16-3 \
                    and self.curt_y-16+3 < question[i].init_y-16 < self.curt_y+16-3:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.isbounce = 20
                self.dy = -6
                return RET_BOUNCE

        down1 = self.gettilemap(self.curt_x+ 2, self.curt_y+16, map_y8)
        down2 = self.gettilemap(self.curt_x+13, self.curt_y+16, map_y8)
        if down1 in NOMOVE or down2 in NOMOVE: # 床あり
            self.dy = 0
            self.curt_y = self.curt_y - (self.curt_y%16)
        else:
            self.dy += 1
            if self.dy > 7:
                self.dy = 7

        if self.dx < 0:
            map1 = self.gettilemap(self.curt_x, self.curt_y   , map_y8)
            map2 = self.gettilemap(self.curt_x, self.curt_y+15, map_y8)
        else:
            map1 = self.gettilemap(self.curt_x+15, self.curt_y   , map_y8)
            map2 = self.gettilemap(self.curt_x+15, self.curt_y+15, map_y8)
        if map1 in NOMOVE or map2 in NOMOVE:
            self.dx *= -1
            self.curt_x += self.dx

        return RET_NONE

class Togezo(Kuribo):
    def attack(self, player_dy):
        return RET_ATTACK

class Kuppa:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.reset()

    def reset(self):
        self.curt_x = self.init_x
        self.curt_y = self.init_y
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0
        self.ptn = 0
        self.alive = 0
        self.dirct = -1
        self.isbreath = 0

    def gettilemap(self, x, y, map_y8):
        if x < 0 or x >= 256*8 or y < map_y8*8 or y >=  map_y8*8+256:
            return -1
        return pyxel.tilemaps[0].pget(x//8, y//8)

    def update(self, map_x, map_y8, player_x, player_y, player_dy, brick, question, firebreath):
        if not self.alive:
            return RET_NONE

        self.dirct = -1 if map_x+player_x-8 < self.curt_x else 1
        if self.isbreath:
            self.isbreath -= 1

        self.ptn += 1

        if self.ddx == 0:
            self.ddx = random.randrange(-10,11)*2
            self.dx = 0
        if self.ddx > 0:
            self.ddx -= 1
            self.dx = 0 if self.ddx%2 else 1
            if self.dx > 0 and self.curt_x > self.init_x+30:
                self.ddx *= -1
        else:
            self.ddx += 1
            self.dx = 0 if self.ddx%2 else -1
            if self.dx < 0 and self.curt_x < self.init_x-30:
                self.ddx *= -1
        self.curt_x += self.dx
        if self.curt_x < map_x-16*4 or self.curt_x > map_x+256+16*2: # 左右スクリーンアウト
            self.reset()
            return RET_SCREENOUT

        self.curt_y += self.dy
        if self.curt_y-map_y8*8 >= 16*16: # 下スクリーンアウト
            self.reset()
            return RET_SCREENOUT

        if self.dirct < 0: # Playerとの接触
            if (self.curt_x-16+3 < player_x+map_x < self.curt_x+16 \
                    and self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+16) or \
                    (self.curt_x-8 < player_x+map_x < self.curt_x+32-3 \
                    and self.curt_y-map_y8*8 < player_y < self.curt_y-map_y8*8+32-3):
                return RET_ATTACK
        else:
            if (self.curt_x < player_x+map_x < self.curt_x+32-3 \
                    and self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+16) or \
                    (self.curt_x-16 < player_x+map_x < self.curt_x+16+8 \
                    and self.curt_y-map_y8*8 < player_y < self.curt_y-map_y8*8+32-3):
                return RET_ATTACK

        for i in range(len(brick)):
            if ((self.dirct<0 and self.curt_x < brick[i].init_x) \
                   or (self.dirct>0 and brick[i].init_x < self.curt_x+32)) \
                    and self.curt_y-5 < brick[i].init_y-32 < self.curt_y+5:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.ddy = 1
                self.dy = -3
                return RET_NONE

        for i in range(len(question)):
            if ((self.dirct<0 and self.curt_x < question[i].init_x) \
                   or (self.dirct>0 and question[i].init_x < self.curt_x+32)) \
                    and self.curt_y-5 < question[i].init_y-32 < self.curt_y+5:
                pyxel.play(3, 2) # Enemy-Damage Sound
                self.ddy = 1
                self.dy = -3
                return RET_NONE

        if self.dirct < 0:
            down1 = self.gettilemap(self.curt_x+16+ 2, self.curt_y+32, map_y8)
            down2 = self.gettilemap(self.curt_x+16+13, self.curt_y+32, map_y8)
        else:
            down1 = self.gettilemap(self.curt_x   + 2, self.curt_y+32, map_y8)
            down2 = self.gettilemap(self.curt_x   +13, self.curt_y+32, map_y8)
        if down1 in NOMOVE or down2 in NOMOVE: # 床あり
            self.dy = 0
            self.curt_y = self.curt_y - (self.curt_y%16)
            if random.randrange(120) == 0: # FireBreath
                if map_x+player_x > self.curt_x+32+32:
                    firebreath.append(FireBreath(self.curt_x+32, self.curt_y+4, \
                             1, self.curt_y+4+random.randrange(2)*16))
                    self.isbreath = 15
                if map_x+player_x < self.curt_x-32:
                    firebreath.append(FireBreath(self.curt_x-24, self.curt_y+4, \
                            -1, self.curt_y+4+random.randrange(2)*16))
                    self.isbreath = 15
            if random.randrange(200) == 0: # 大ジャンプ
                self.ddy = 1
                self.dy = -6
            if random.randrange(100) == 0: # 小ジャンプ
                self.ddy = 1
                self.dy = -4
        else:
            if self.dy < 0:
                self.ddy -= 1
                if self.ddy < 0:
                    self.dy += 1
                    self.ddy = 2
            else:
                self.dy += 1
                if self.dy > 7:
                    self.dy = 7

        if self.dx < 0:
            map1 = self.gettilemap(self.curt_x+3   , self.curt_y+16   , map_y8)
            map2 = self.gettilemap(self.curt_x+3   , self.curt_y+16+15, map_y8)
        else:
            map1 = self.gettilemap(self.curt_x+32-3, self.curt_y+16   , map_y8)
            map2 = self.gettilemap(self.curt_x+32-3, self.curt_y+16+15, map_y8)
        if map1 in NOMOVE or map2 in NOMOVE:
            self.dx *= -1
            self.curt_x += self.dx
        return RET_NONE

class FireBreath:
    def __init__(self, x, y, dx, target_y):
        self.curt_x = x
        self.curt_y = y
        self.dx = dx
        self.target_y = target_y

    def update(self, map_x, map_y8, player_x, player_y, player_dy):
        self.curt_x += self.dx*2
        if self.curt_y > self.target_y:
            self.curt_y -= 1
        if self.curt_y < self.target_y:
            self.curt_y += 1

        if self.curt_x < map_x-16*2 or self.curt_x > map_x+256+16:
            return RET_SCREENOUT
        if self.curt_x-16+5 < map_x+player_x < self.curt_x+24-5 and \
                self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+8-3:
                return RET_ATTACK
        return RET_NONE

class HodaiKiller:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.reset()

    def reset(self):
        self.curt_y = self.init_y
        self.dy = 0
        self.cntdwn = 30
        self.alive = 0

    def update(self, map_x, map_y8, player_x, player_y, player_dy):
        if self.alive:
            if self.dx:
                self.curt_x += self.dx
                if self.curt_x < map_x-16*2 or self.curt_x > map_x+256+16:
                    self.reset()
                    return RET_SCREENOUT
                if self.curt_x-16+3 < map_x+player_x < self.curt_x+16-3 and \
                        self.curt_y-map_y8*8-16+3 < player_y < self.curt_y-map_y8*8+16-3:
                    if player_dy > 0:
                        self.dx = 0
                        return RET_STOMPED
                    else:
                        return RET_ATTACK
            else:
                self.dy += 1
                self.curt_y += self.dy
                if self.curt_y-map_y8*8 >= 16*16:
                    self.reset()
                    return RET_SCREENOUT
            return RET_NONE
        else:
            if self.init_y//256 == map_y8//32 and (map_x-16 <= self.init_x < map_x+player_x-16*3 or \
                    map_x+player_x+16*3 <= self.init_x < map_x+256):
                self.cntdwn -= 1
                if self.cntdwn <= 0:
                    self.cntdwn = 30
                    if map_x+player_x < self.init_x:
                        self.dirct = -1
                        self.dx = -3
                        self.curt_x = self.init_x-8
                    else:
                        self.dirct = 1
                        self.dx = 3
                        self.curt_x = self.init_x+8
                    self.alive = 1
            else:
                self.cntdwn = 30
        return RET_NONE

class RandomKiller:
    def __init__(self, map_x):
        if random.randrange(2) == 0:
            self.dirct = -1
            self.dx = -3
            self.curt_x = map_x+256+16
        else:
            self.dirct = 1
            self.dx = 3
            self.curt_x = map_x-16*2
        self.curt_y = random.randrange(12)*16+16
        self.dy = 0

    def update(self, map_x, map_y8, player_x, player_y, player_dy):
        if self.dx:
            self.curt_x += self.dx
            if self.curt_x < map_x-16*2 or self.curt_x > map_x+256+16:
                return RET_SCREENOUT
            if self.curt_x-16+3 < map_x+player_x < self.curt_x+16-3 and \
                    self.curt_y-16+3 < player_y < self.curt_y+16-3:
                if player_dy > 0:
                    self.dx = 0
                    return RET_STOMPED
                else:
                    return RET_ATTACK
        else:
            self.dy += 1
            self.curt_y += self.dy
            if self.curt_y-map_y8*8 >= 16*16:
                return RET_SCREENOUT
        return RET_NONE

class Rescue:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.reset()

    def reset(self):
        self.curt_x = self.init_x
        self.curt_y = self.init_y
        self.dy = 0
        self.alive = 0

    def gettilemap(self, x, y, map_y8):
        if x < 0 or x >= 256*8 or y < map_y8*8 or y >=  map_y8*8+256:
            return -1
        return pyxel.tilemaps[0].pget(x//8, y//8)

    def update(self, map_x, map_y8, player_x, player_y, player_dy):
        if not self.alive:
            return RET_NONE
        if self.curt_x < map_x-16*2 or self.curt_x > map_x+256+16:
            self.alive = 0
            return RET_SCREENOUT
        if self.curt_x-16 < player_x+map_x < self.curt_x+16 \
                and self.curt_y-map_y8*8-16 < player_y < self.curt_y-map_y8*8+24:
            return RET_TOUCH
        return RET_NONE

App()

