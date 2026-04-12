from game import games
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()

# player 1 - turquoise
# player 2 - pink


#colors
boardcol = (0,236,255)
col1 = (103,21,255)
col2 = (255,0,127)
win = (255,136,0)
BLACK = (0,0,0)

FPS = pygame.time.Clock()
FPS.tick(60)
end_time=None

class Connect(games):
    def occ(self,x,y):
        if (self.board[x,y] == 0):
            return False
        else:
            return True
    def column(self,pos):
        if pos[0]>=100 and pos[0]<800 :
            column = (pos[0]-100)//100
            return column
        else:
            return -1
    def available_row(self,column):
        for i in range(6,-1,-1):
            if(self.occ(i,column) == False):
                return i
        return -1
            
    def win_check(self):
        rows, cols = self.board.shape
        length = 4
        t = self.board == self.active #truth matrix
        #we use binary logic to check 
        #for horizontal
        h = t[:,0:0+length] & t[:,1:1+length] & t[:,2:2+length] & t[:,3:length+3]
        if np.any(h):
            posn = np.where(h == 1)
            self.board[posn[0][0],posn[1][0]:posn[1][0]+length] = -1
            return self.active
        #for vertical
        v = t[0:0+length,:] & t[1:1+length,:] & t[2:2+length,:] & t[3:length+3,:] 
        if np.any(v):        
            posn = np.where(v == 1)
            self.board[posn[0][0]:posn[0][0]+length,posn[1][0]] = -1
            return self.active
        #top left to bottom right diagonal
        d1 = t[0:length,0:length] &   t[1:1+length,1:1+length] & t[2:2+length,2:2+length] & t[3:length+3,3:length+3] 
        if np.any(d1):
            posn = np.where(d1 == 1)
            self.board[(posn[0][0],posn[0][0]+1,posn[0][0]+2,posn[0][0]+3),(posn[1][0],posn[1][0]+1,posn[1][0]+2,posn[1][0]+3)] = -1
            return self.active
        #bottom left to top right
        d2 = t[rows-length:rows,0:0+length] & t[rows-length-1:rows-1,1:1+length] & t[rows-length-2:rows-2,2:2+length] & t[rows-length-3:rows-3,3:length+3]
        if np.any(d2):
            posn = np.where(d2 == 1)
            self.board[(posn[0][0]+3,posn[0][0]+2,posn[0][0]+1,posn[0][0]),(posn[1][0],posn[1][0]+1,posn[1][0]+2,posn[1][0]+3)] = -1
            return self.active
        return 0
    def execution(self):
        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(49).reshape((7,7))
        FPS = pygame.time.Clock()
        FPS.tick(60)
        end_time=None
        pygame.display.set_caption("Connect 4")
        game_on = True

        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos
                    c = self.column(position)
                    if c >= 0 :
                        row = self.available_row(c)
                        if row >= 0:
                            self.board[row,c] = self.active
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
            pygame.draw.rect(display, boardcol, (100,225,700,525))
        
            for r in range(7):
                for c in range(7):
                    if self.board[r,c] == 1 :
                        pygame.draw.circle(display, col1 , (150+100*(c),275 + 70*(r)), 30)
                    elif self.board[r,c] == 2:
                        pygame.draw.circle(display, col2 , (150+100*(c),275 + 70*(r)), 30)
                    elif self.board[r,c] == -1:
                        pygame.draw.circle(display, win , (150+100*(c),275 + 70*(r)), 30)
                    elif self.board[r,c] == 0:
                        pygame.draw.circle(display, BLACK , (150+100*(c),275 + 70*(r)), 30)
    
            if not game_on and time.time()-end_time>1.25:
                font = pygame.font.SysFont(None, 72)
                if self.winner != 0:
                    text = font.render(f"Player {self.winner} Wins!", True, win)
                else:
                    text = font.render("It's a Draw!", True, win)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, win , rect.inflate(40, 40), 5)
                display.blit(text, rect)
    
            pygame.display.update()

