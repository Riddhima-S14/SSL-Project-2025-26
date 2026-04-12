from game import games
import numpy as np
import time
import pygame
from pygame.locals import *
pygame.init()

#player 1 - circle - 1
#player 2 - cross - 2 
#colors

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Tictactoe(games):
    def occ(self,x,y):
        if self.board[x,y] == 0:
            return False
        else:
            return True
    def box(self,posn):
        if posn[0]<100 or posn[0]>800 or posn[1]<25 or posn[1]>725 :
            return((-1,-1))
        else:
            x = (posn[0]-100)//70
            y = (posn[1]-25)//70
            return((y,x))
    def win_check(self):
        rows, cols = self.board.shape
        length = 5
        t = self.board == self.active #truth matrix
        #we use binary logic to check 
        #for horizontal
        h = t[:,0:0+length+1] & t[:,1:2+length] & t[:,2:3+length] & t[:,3:length+4] & t[:,4:length+5]
        if np.any(h):
            posn = np.where(h == 1)
            self.win_line = ((135+posn[1][0]*70,60+posn[0][0]*70),(4*70+135+posn[1][0]*70,60+posn[0][0]*70))
            return self.active
        #for vertical
        v = t[0:0+length+1,:] & t[1:2+length,:] & t[2:3+length,:] & t[3:length+4,:] & t[4:length+5,:]
        if np.any(v):
            posn = np.where(v ==1) 
            self.win_line = ((135+int(posn[1][0])*70,60+int(posn[0][0])*70),(135+int(posn[1][0])*70,4*70+60+int(posn[0][0])*70))        
            return self.active
        #top left to bottom right diagonal
        d1 = t[0:0+length+1,0:0+length+1] &   t[1:2+length,1:2+length] & t[2:3+length,2:3+length] & t[3:length+4,3:length+4] & t[4:length+5,4:length+5]
        if np.any(d1):
            posn = np.where(d1 == 1)
            self.win_line = ((135+posn[1][0]*70,60+posn[0][0]*70),(4*70+135+posn[1][0]*70,4*70+60+posn[0][0]*70))
            return self.active
        #bottom left to top right
        d2 = t[rows-1:rows-1-length-1,0:0+length+1] & t[rows-2:rows-length-3,1:2+length] & t[rows-3:rows-length-4,2:3+length] & t[rows-4:rows-length-5,4:length+5]
        if np.any(d2):
            posn = np.where(d2 == 1)
            self.win_line = ((135+(posn[1][0])*70,60+(posn[0][0]+4)*70),(4*70+135+posn[1][0]*70,60+(posn[0][0]+4)*70-4*70))
            return self.active
        return 0 
    def draw_cross(self,surface, color, center_pos, size):
        x, y = center_pos
        pygame.draw.line(surface, color, (x - size+5, y - size), (x + size-5, y + size),5)
        pygame.draw.line(surface, color, (x + size-5, y - size), (x - size+5, y + size),5)
    def execution(self):
        FPS = pygame.time.Clock()
        FPS.tick(60)
        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(100).reshape((10,10))
        pygame.display.set_caption("Tic Tac Toe")
        game_on=True
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos
                    g_box = self.box(position)
                    if (g_box[0] >= 0):
                        if (self.occ(g_box[0],g_box[1]) == False):
                            self.board[g_box[0],g_box[1]] = self.active
                            winner=self.win_check()                     
                            if winner!=0:
                                self.winner=self.active
                                end_time=time.time()
                                game_on=False
                            elif not np.any(self.board == 0):
                        #draw
                                end_time=time.time()
                                game_on=False
                            else:
                                self.switch()
                elif not game_on and event.type == pygame.KEYDOWN:
                    pygame.quit()
                    exit()

            display.fill(BLACK)
            for i in range(1,10):
                pygame.draw.line(display,GREEN,(100,25+70*i),(800,25+70*i),3)
                pygame.draw.line(display,GREEN,(100+70*i,25), (100+70*i,725),3)
            for i in range(10):
                for j in range(10):
                    if self.board[j,i] == 1:
                        pygame.draw.circle(display, BLUE, (135+70*i,60+70*j), 25)
                        pygame.draw.circle(display, BLACK, (135+70*i,60+70*j), 20)

                    elif self.board[j,i] == 2:
                        self.draw_cross(display,RED,(135+70*i,60+70*j),25)
            if not game_on and self.win_line:
                pygame.draw.line(display, WHITE, self.win_line[0], self.win_line[1], 8)
            if not game_on and time.time()-end_time>1.25:
                font = pygame.font.SysFont(None, 72)
                if self.winner != 0:
                    text = font.render(f"Player {self.winner} Wins!", True, GREEN)
                else:
                    text = font.render("It's a Draw!", True, GREEN)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, GREEN, rect.inflate(40, 40), 5)
                display.blit(text, rect)
            pygame.display.update()    
            
