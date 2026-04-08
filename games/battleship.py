from game import games
import numpy as np
import time
import pygame
import random
from pygame.locals import *

pygame.init()

display=pygame.display.set_mode((900, 750))
pygame.display.set_caption("Battleship")

# colours
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)

FPS=pygame.time.Clock()
FPS.tick(60)

CELL_SIZE=40
ROWS, COLS=7, 10


TOP_OFFSET=25
BOTTOM_OFFSET=25+CELL_SIZE*ROWS+65
CENTER_OFFSET=CELL_SIZE//2 

board_p1=np.zeros((ROWS, COLS))
board_p2=np.zeros((ROWS, COLS))

ships=[5, 4, 3, 3, 2]

def place_ships(board):
    for ship in ships:
        placed=False
        while not placed:
            orientation=random.choice(["H", "V"])
            if orientation=="H":
                r=random.randint(0, ROWS-1)
                c=random.randint(0, COLS-ship)
                if np.all(board[r, c:c+ship]==0):
                    board[r, c:c+ship]=1
                    placed=True
            else:
                r=random.randint(0, ROWS-ship)
                c=random.randint(0, COLS-1)
                if np.all(board[r:r+ship, c]==0):
                    board[r:r+ship, c]=1
                    placed=True
    


class Battleship(games):
    def __init__(self, player1, player2, board_size=(10, 10)):
        super().__init__(player1, player2, np.zeros(board_size))
        self.board_p1=np.zeros(board_size)
        self.board_p2=np.zeros(board_size)
        place_ships(self.board_p1)
        place_ships(self.board_p2)
        self.hits_p1=np.zeros(board_size)
        self.hits_p2=np.zeros(board_size)
    
    def box(self, posn):
       #top board
        if 250<=posn[0]<=650 and TOP_OFFSET<=posn[1]<=TOP_OFFSET+CELL_SIZE*ROWS:
            x=(posn[0]-250)//CELL_SIZE
            y=(posn[1]-TOP_OFFSET)//CELL_SIZE
            return (y, x, 1)

       #bottom board
        elif 250<=posn[0]<=650 and BOTTOM_OFFSET<=posn[1]<=BOTTOM_OFFSET+CELL_SIZE*ROWS:
            x=(posn[0]-250)//CELL_SIZE
            y=(posn[1]-BOTTOM_OFFSET)//CELL_SIZE
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


play=Battleship(1, 2, (ROWS, COLS))
game_on=True
end_time=None

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()

        elif game_on and event.type==pygame.MOUSEBUTTONDOWN:
            pos=event.pos
            y, x, target=play.box(pos)

            if target!=-1:
                if (play.active==1 and target==2) or (play.active==2 and target==1):
                    if play.fire((y, x)):

                        if target==2 and play.board_p2[y, x]==1:
                            pass
                        elif target==1 and play.board_p1[y, x]==1:
                            pass
                        else:
                            play.switch()

                        winner=play.win_check()
                        if winner:
                            play.winner=winner
                            end_time=time.time()
                            game_on=False

        elif not game_on and event.type==pygame.KEYDOWN:
            pygame.quit()
            exit()

    display.fill(BLACK)

    #draw grids
    
    for i in range(1, ROWS):
        pygame.draw.line(display, WHITE, (250, TOP_OFFSET + CELL_SIZE*i), (250 + CELL_SIZE*COLS, TOP_OFFSET + CELL_SIZE*i), 2)
        pygame.draw.line(display, WHITE, (250, BOTTOM_OFFSET + CELL_SIZE*i), (250 + CELL_SIZE*COLS, BOTTOM_OFFSET + CELL_SIZE*i), 2)

    for i in range(1, COLS):
        pygame.draw.line(display, WHITE, (250 + CELL_SIZE*i, TOP_OFFSET), (250 + CELL_SIZE*i, TOP_OFFSET + CELL_SIZE*ROWS), 2)
        pygame.draw.line(display, WHITE, (250 + CELL_SIZE*i, BOTTOM_OFFSET), (250 + CELL_SIZE*i, BOTTOM_OFFSET + CELL_SIZE*ROWS), 2)

    #divider
    pygame.draw.line(display, WHITE, (200, BOTTOM_OFFSET-25), (700, BOTTOM_OFFSET-25), 4)

    
    for y in range(ROWS):
        for x in range(COLS):
            if play.hits_p2[y, x]==1:
                px=250+CENTER_OFFSET+CELL_SIZE*x
                py=BOTTOM_OFFSET+CENTER_OFFSET+CELL_SIZE*y
                if play.board_p2[y, x]==1:
                    pygame.draw.circle(display, GREEN, (px, py), 15)
                else:
                    pygame.draw.circle(display, WHITE, (px, py), 15)

   
    for y in range(ROWS):
        for x in range(COLS):
            if play.hits_p1[y, x]==1:
                px=250+CENTER_OFFSET+CELL_SIZE*x
                py=TOP_OFFSET+CENTER_OFFSET+CELL_SIZE*y
                if play.board_p1[y, x]==1:
                    pygame.draw.circle(display, BLUE, (px, py), 15)
                else:
                    pygame.draw.circle(display, WHITE, (px, py), 15)

    if not game_on and time.time()-end_time > 1.25:
        font=pygame.font.SysFont(None, 72)
        if play.winner!=0:
            text=font.render(f"Player {play.winner} Wins!", True, WHITE)
        else:
            text=font.render("It's a Draw!", True, WHITE)

        rect=text.get_rect(center=(450, 375))
        pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
        pygame.draw.rect(display, GREEN, rect.inflate(40, 40), 5)
        display.blit(text, rect)

    pygame.display.update()