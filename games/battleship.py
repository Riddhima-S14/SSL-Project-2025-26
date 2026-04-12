from game import games
import numpy as np
import time
import pygame
import random
from pygame.locals import *

pygame.init()

# colours
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)

class Battleship(games):
    def __init__(self, player1, player2, board_size=(10, 10)):
        super().__init__(player1, player2, np.zeros(board_size))
        self.board_p1=np.zeros(board_size)
        self.board_p2=np.zeros(board_size)
        self.place_ships(self.board_p1)
        self.place_ships(self.board_p2)
        self.hits_p1=np.zeros(board_size)
        self.hits_p2=np.zeros(board_size)
    def place_ships(self,board):
        ships=[5, 4, 3, 3, 2]
        for ship in ships:
            placed=False
            while not placed:
                orientation=random.choice(["H", "V"])
                if orientation=="H":
                    r=random.randint(0, 7-1) #rows - 1
                    c=random.randint(0, 10-ship) #columns - ship
                    if np.all(board[r, c:c+ship]==0):
                        board[r, c:c+ship]=1
                        placed=True
                else:
                    r=random.randint(0, 7-ship) #rows - ship
                    c=random.randint(0, 10-1) #cols - 1
                    if np.all(board[r:r+ship, c]==0):
                        board[r:r+ship, c]=1
                        placed=True
    def box(self, posn):
        CELL_SIZE=40
        ROWS, COLS=7, 10
        TOP_OFFSET=25
        BOTTOM_OFFSET=25+CELL_SIZE*ROWS+40
        CENTER_OFFSET=CELL_SIZE//2
       #top board
        if 250<=posn[0]<=650 and TOP_OFFSET<=posn[1]<=TOP_OFFSET+CELL_SIZE*ROWS:
            x=(posn[0]-250)//CELL_SIZE
            y=(posn[1]-TOP_OFFSET)//CELL_SIZE
            return (y, x, 1)

       #bottom board
        elif 250<=posn[0]<=650 and BOTTOM_OFFSET+25<=posn[1]<=BOTTOM_OFFSET+CELL_SIZE*ROWS + 25:
            x=(posn[0]-250)//CELL_SIZE
            y=(posn[1]-BOTTOM_OFFSET-25)//CELL_SIZE
            return (y, x, 2)

        return (-1, -1, -1)

    def fire(self, target):
        y, x=target
        if self.active==1:
            if self.hits_p2[y, x]==0:
                self.hits_p2[y, x]=1
                return True
        else:
            if self.hits_p1[y, x]==0:
                self.hits_p1[y, x]=1
                return True
        return False

    def win_check(self):
        if np.all((self.hits_p2==1) | (self.board_p2==0)):
            return self.player1
        elif np.all((self.hits_p1==1) | (self.board_p1==0)):
            return self.player2
        return 0
    def execution(self):

        #design info
        CELL_SIZE=40
        ROWS, COLS=7, 10
        TOP_OFFSET=25
        BOTTOM_OFFSET=25+CELL_SIZE*ROWS+40
        CENTER_OFFSET=CELL_SIZE//2

        board_p1=np.zeros((ROWS, COLS))
        board_p2=np.zeros((ROWS, COLS))

        display=pygame.display.set_mode((900, 750))
        pygame.display.set_caption("Battleship")
        game_on=True
        end_time=None
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()

                elif game_on and event.type==pygame.MOUSEBUTTONDOWN:
                    pos=event.pos
                    y, x, target=self.box(pos)

                    if target!=-1:
                        if (self.active==1 and target==2) or (self.active==2 and target==1):
                            if self.fire((y, x)):

                                if target==2 and self.board_p2[y, x]==1:
                                    pass
                                elif target==1 and self.board_p1[y, x]==1:
                                    pass
                                else:
                                    self.switch()

                                winner=self.win_check()
                                if winner:
                                    self.winner=winner
                                    end_time=time.time()
                                    game_on=False

                elif not game_on and event.type==pygame.KEYDOWN:
                    pygame.quit()
                    exit()

            display.fill(BLACK)

    #draw grids
    
            for i in range(1, ROWS):
                pygame.draw.line(display, WHITE, (250, TOP_OFFSET + CELL_SIZE*i), (250 + CELL_SIZE*COLS, TOP_OFFSET + CELL_SIZE*i), 2)
                pygame.draw.line(display, WHITE, (250, 25 + BOTTOM_OFFSET + CELL_SIZE*i), (250 + CELL_SIZE*COLS, 25+ BOTTOM_OFFSET + CELL_SIZE*i), 2)

            for i in range(1, COLS):
                pygame.draw.line(display, WHITE, (250 + CELL_SIZE*i, TOP_OFFSET), (250 + CELL_SIZE*i, TOP_OFFSET + CELL_SIZE*ROWS), 2)
                pygame.draw.line(display, WHITE, (250 + CELL_SIZE*i, 25 + BOTTOM_OFFSET), (250 + CELL_SIZE*i, 25 + BOTTOM_OFFSET + CELL_SIZE*ROWS), 2)

            #divider
            pygame.draw.line(display, WHITE, (200, BOTTOM_OFFSET), (700, BOTTOM_OFFSET), 4)

    
            for y in range(ROWS):
                for x in range(COLS):
                    if self.hits_p2[y, x]==1:
                        px=250+CENTER_OFFSET+CELL_SIZE*x
                        py=BOTTOM_OFFSET+CENTER_OFFSET+CELL_SIZE*y + 25
                        if self.board_p2[y, x]==1:
                            pygame.draw.circle(display, GREEN, (px, py), 17)
                        else:
                            pygame.draw.circle(display, WHITE, (px, py), 17)

   
            for y in range(ROWS):
                for x in range(COLS):
                    if self.hits_p1[y, x]==1:
                        px=250+CENTER_OFFSET+CELL_SIZE*x
                        py=TOP_OFFSET+CENTER_OFFSET+CELL_SIZE*y
                        if self.board_p1[y, x]==1:
                            pygame.draw.circle(display, BLUE, (px, py), 17)
                        else:
                            pygame.draw.circle(display, WHITE, (px, py), 17)

            if not game_on and time.time()-end_time > 1.25:
                font=pygame.font.SysFont(None, 72)
                if self.winner !=0 :
                    text=font.render(f"Player {self.winner} Wins!", True, GREEN)
                else:
                    text=font.render("It's a Draw!", True, GREEN)

                rect=text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, GREEN, rect.inflate(40, 40), 5)
                display.blit(text, rect)

            pygame.display.update()


# play=Battleship(1, 2, (7, 10))
# play.execution()
