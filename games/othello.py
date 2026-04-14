#othello
from game import games
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()



#player 1 - 1 - col 1
#player 2 - -1 - col 2

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
boardcol = (0,236,255)
col1 = (103,21,255)
col2 = (255,0,127)
wincol = (255,136,0)


class othello(games):
    def occ(self,x,y):
        if (self.board[x,y] == 0):
            return False
        else:
            return True
    def box(self,posn):
        if posn[0]<130 or posn[0]>770 or posn[1]<55 or posn[1]>695 :
            return((-1,-1))
        else:
            x = (posn[0]-130)//80
            y = (posn[1]-55)//80
            return((y,x))
        
    def valid(self, a):
        return np.all((a>=0) & (a<8), axis = 1)

    def finding_valid(self, box, check=False):
        r,c = box[0],box[1]
        matrix = (self.board[max(r-1,0):min(8,r+2),max(c-1,0):min(8,c+2)] == self.n_active)
        print(matrix)
        valid = False
        if np.any(matrix):
            pos_r = 1 if r > 0 else 0
            pos_c = 1 if c>0 else 0 
            direction = np.argwhere(matrix == 1) - [pos_r,pos_c]
            print(direction)
            #slice_end = (direction == 1)*8 + (direction == 0)*[r,c]
            #horizontal
            if any(np.all(direction == [0, 1], axis=1)):
                pieces = np.argmin(self.board[r,c+1:] == self.n_active)
                if pieces > 0 and self.board[r,min(c+1+pieces,7)] == self.active:
                    if check:
                        return True
                    self.board[r,c+1:c+pieces+1] = self.active
            if any(np.all(direction == [0, -1], axis=1)):
                pieces = np.argmin(self.board[r,c-1::-1] == self.n_active)
                if pieces > 0 and self.board[r,max(c-pieces-1,0) ] == self.active:
                    if check:
                        return True
                    self.board[r,c-pieces:c] = self.active
            #vertical
            if any(np.all(direction == [1,0], axis=1)):
                print("yes")
                pieces = np.argmin(self.board[r+1:,c] == self.n_active)
                print(pieces)
                if pieces > 0 and self.board[min(r+1+pieces,7),c] == self.active:
                    if check:
                        return True
                    self.board[r+1:r+pieces+1,c] = self.active
            if any(np.all(direction == [-1,0], axis=1)):
                pieces = np.argmin(self.board[r-1::-1,c] == self.n_active)
                if pieces > 0 and self.board[max(r-pieces-1,0),c] == self.active:
                    if check:
                        return True
                    self.board[r-pieces:r,c] = self.active
            #top left diagonal
            if any(np.all(direction == [1,1], axis=1)):
                pieces = np.argmin(np.diagonal(self.board[r+1:,c+1:]) == self.n_active)
                if pieces > 0 and self.board[min(7,r+1+pieces),min(7,c+1+pieces)] == self.active:
                    if check:
                        return True
                    self.board[r+1:r+1+pieces,c+1:c+1+pieces] += np.eye(pieces)*(self.active-self.n_active)
            if any(np.all(direction == [-1,-1], axis=1)):
                pieces = np.argmin(np.diagonal(self.board[r-1::-1,c-1::-1]) == self.n_active)
                if pieces > 0 and self.board[max(r-pieces-1,0),max(c-pieces-1,0)] == self.active:
                    if check:
                        return True
                    self.board[r-pieces:r,c-pieces:c] += np.eye(pieces)*(self.active-self.n_active)
            #top right diagonal
            if any(np.all(direction == [1,-1], axis=1)):
                pieces = np.argmin(np.diagonal((self.board[r+1:,c-1::-1])) == self.n_active)
                print(pieces)
                if pieces > 0 and self.board[min(7,r+1+pieces),max(c-pieces-1,0)] == self.active:
                    if check:
                        return True
                    self.board[r+1:r+1+pieces,c-pieces:c] += np.fliplr(np.eye(pieces)*(self.active-self.n_active))
            if any(np.all(direction == [-1, 1], axis=1)):
                pieces = np.argmin(np.diagonal((self.board[r-1::-1,c+1:])) == self.n_active)
                print(pieces)
                if pieces > 0 and self.board[max(r-pieces-1,0), min(7,c+1+pieces)] == self.active:
                    if check:
                        return True
                    self.board[r-pieces:r,c+1:c+1+pieces] += np.fliplr(np.eye(pieces)*(self.active-self.n_active))
            if check:
                return False
    def valid_left(self):
        for i in range(8):
            for j in range(8):
                if self.finding_valid((i, j),True):
                    return True    
        return True    
    def win_check(self):
        score1 = np.sum(self.board == 1)
        score2 = np.sum(self.board == 2)
        if score1 > score2:
            return 1
        elif score2 > score1:
            return 2
        return 0
    def execution(self):

        pygame.display.set_caption("Othello")
        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(64).reshape((8,8))
        self.board[3,3],self.board[4,4],self.board[3,4],self.board[4,3] = 1,1,2,2

        FPS = pygame.time.Clock()

        end_time=None
        game_on = True
        while True:
            FPS.tick(60)
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos
                    box = self.box(position)
                    if ( box[0]!=-1 ):
                        valid_moves = self.valid_left()
                        if (valid_moves == False):
                            self.switch()
                            if(self.valid_left() == False ):
                                win = self.win_check()
                                if win!=0:
                                    self.winner = win
                                    end_time=time.time()
                                    game_on=False
                                else:
                                    end_time=time.time()
                                    game_on=False
                        else:
                            move = self.finding_valid(box,True)
                            if(move):
                                self.finding_valid(box)
                                self.board[box] = self.active
                                if (np.any(self.board == 0) == False):
                                    win = self.win_check()
                                    if win!=0:
                                        self.winner = win
                                        end_time=time.time()
                                        game_on=False
                                    else:
                                        end_time=time.time()
                                        game_on=False
                                else:
                                    self.switch()
                elif not game_on and event.type == pygame.KEYDOWN:
                    pygame.quit()
                    exit()

            display.fill(BLACK)
            for i in range(1,8):
                pygame.draw.line(display,GREEN,(130,55+80*i),(770,55+80*i),3)
                pygame.draw.line(display,GREEN,(130+80*i,55), (130+80*i,695),3)
            for i in range(8):
                for j in range(8):
                    if self.board[j,i] == 1:
                        pygame.draw.circle(display, col1, (170+80*i,95+80*j),35)
                    elif self.board[j,i] == 2:
                        pygame.draw.circle(display, col2, (170+80*i,95+80*j),35)
            font = pygame.font.SysFont(None, 72)
            score_str1 = f"{np.sum(self.board == 1)}"
            score_surf1 = font.render(score_str1, True, col1)
            score_str2 = f"{np.sum(self.board == 2)}"
            score_surf2 = font.render(score_str2, True, col2)
            display.blit(score_surf1, (65,375))
            display.blit(score_surf2,(770+65,375))
             
            if not game_on and time.time()-end_time>0.75:
                font = pygame.font.SysFont(None, 72)
                if self.winner != 0:
                    text = font.render(f"Player {self.winner} Wins!", True, wincol)
                else:
                    text = font.render("It's a Draw!", True, wincol)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, wincol , rect.inflate(40, 40), 5)
                display.blit(text, rect)
    
            pygame.display.update()
# play = othello(1,2)
# play.execution()
