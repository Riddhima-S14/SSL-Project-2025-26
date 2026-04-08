from game import games
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()

# player 1 - turquoise
# player 2 - pink

display = pygame.display.set_mode((900,750))
board = np.zeros(49).reshape((7,7))

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

        for r in range(rows):
            for c in range(cols-length+1):
                slice=self.board[r, c:c+length]
                if np.all(slice==self.active):
                    for i in range(length):
                        self.board[r,c+i] = -1
                    return self.active
        
        for c in range(cols):
            for r in range(rows-length+1):
                slice=self.board[r:r+length, c]
                if np.all(slice==self.active):
                    for i in range(length):
                        self.board[r+i,c] = -1
                    return self.active
                
        for r in range(rows-length+1):
            for c in range(cols-length+1):
                slice=self.board[r:r+length, c:c+length]
                if np.all(np.diagonal(slice)==self.active):
                    for i in range(length):
                        self.board[r+i,c+i] = -1
                    return self.active
        
        for r in range(rows-length+1):
            for c in range(rows-length+1):
                slice=self.board[r:r+length, c:c+length]
                flipped=np.diagonal(np.fliplr(slice))
                if np.all(flipped==self.active):
                    for i in range(length):
                        self.board[r+length-1-i,c+i] = -1
                    return self.active
        
        return 0

pygame.display.set_caption("Connect 4")

play = Connect(1,2,board)
game_on = True

while True:
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
        elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            c = play.column(position)
            if c >= 0 :
                row = play.available_row(c)
                if row >= 0:
                    play.board[row,c] = play.active
                    winner=play.win_check()                     
                    if winner!=0:
                        play.winner=play.active
                        end_time=time.time()
                        game_on=False
                    elif not np.any(play.board == 0):
                        #draw
                        end_time=time.time()
                        game_on=False
                    else:
                        play.switch()
        elif not game_on and event.type == pygame.KEYDOWN:
            pygame.quit()
            exit()
    
    display.fill(BLACK)
    pygame.draw.rect(display, boardcol, (100,225,700,525))
        
    for r in range(7):
        for c in range(7):
            if play.board[r,c] == 1 :
                pygame.draw.circle(display, col1 , (150+100*(c),275 + 70*(r)), 30)
            elif play.board[r,c] == 2:
                pygame.draw.circle(display, col2 , (150+100*(c),275 + 70*(r)), 30)
            elif play.board[r,c] == -1:
                pygame.draw.circle(display, win , (150+100*(c),275 + 70*(r)), 30)
            elif play.board[r,c] == 0:
                pygame.draw.circle(display, BLACK , (150+100*(c),275 + 70*(r)), 30)
    
    if not game_on and time.time()-end_time>1.25:
        font = pygame.font.SysFont(None, 72)
        if play.winner != 0:
            text = font.render(f"Player {play.winner} Wins!", True, win)
        else:
            text = font.render("It's a Draw!", True, win)
        rect = text.get_rect(center=(450, 375))
        pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
        pygame.draw.rect(display, win , rect.inflate(40, 40), 5)
        display.blit(text, rect)
    
    pygame.display.update()

