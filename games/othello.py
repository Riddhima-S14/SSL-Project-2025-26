#othello
from game import games_class
import numpy as np
import pygame
import os
import time
from pygame.locals import *
pygame.init()



#player 1 - 1 - col 1
#player 2 - -1 - col 2
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW=(255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
boardcol = (0,236,255)
col1 = (103,21,255)
col2 = (255,0,127)
wincol = (255,136,0)


class othello(games_class):

    BASE_PATH=os.path.dirname(__file__)
    ASSETS_DIR=os.path.join(BASE_PATH, '../assets')

    font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
    font_big=pygame.font.Font(font_path, 50)
    font_medium=pygame.font.Font(font_path, 32)
    font_small=pygame.font.Font(font_path, 18)
    font_name=pygame.font.Font(font_path, 14)

    bg_main=pygame.image.load(os.path.join(ASSETS_DIR, "othello_bg.png")).convert()

    def occ(self,x,y):
        if (self.board[x,y] == 0):
            return False
        else:
            return True
    def box(self,posn):
        if posn[0]<210 or posn[0]>690 or posn[1]<170 or posn[1]>650 :
            return((-1,-1))
        else:
            x = (posn[0]-210)//60
            y = (posn[1]-170)//60
            return((y,x))
        
    def valid(self, a):
        return np.all((a>=0) & (a<8), axis = 1)

    def finding_valid(self, box, check=False):
        r,c = box[0],box[1]
        if box[0]>-1 and self.occ(r,c):
            return False
        matrix = (self.board[max(r-1,0):min(8,r+2),max(c-1,0):min(8,c+2)] == self.n_active)
        valid = False
        if np.any(matrix):
            pos_r = 1 if r > 0 else 0
            pos_c = 1 if c>0 else 0 
            direction = np.argwhere(matrix == 1) - [pos_r,pos_c]
            #slice_end = (direction == 1)8 + (direction == 0)[r,c]
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
                pieces = np.argmin(self.board[r+1:,c] == self.n_active)
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
                if pieces > 0 and self.board[min(7,r+1+pieces),max(c-pieces-1,0)] == self.active:
                    if check:
                        return True
                    self.board[r+1:r+1+pieces,c-pieces:c] += np.fliplr(np.eye(pieces)*(self.active-self.n_active))
            if any(np.all(direction == [-1, 1], axis=1)):
                pieces = np.argmin(np.diagonal((self.board[r-1::-1,c+1:])) == self.n_active)
                if pieces > 0 and self.board[max(r-pieces-1,0), min(7,c+1+pieces)] == self.active:
                    if check:
                        return True
                    self.board[r-pieces:r,c+1:c+1+pieces] += np.fliplr(np.eye(pieces)*(self.active-self.n_active))
            if check:
                return False
    def valid_left(self):
        for i in range(8):
            for j in range(8):
                if not self.occ(i,j) and self.finding_valid((i, j),True):
                    return True    
        return False    
    def win_check(self):
        score1 = np.sum(self.board == 1)
        score2 = np.sum(self.board == 2)
        if score1 > score2:
            return self.player1
        elif score2 > score1:
            return self.player2
        return 0
    def show(self,screen, mouse_pos):
        screen.blit(self.bg_main, (0, 0))

        p1_label=self.font_name.render("PLAYER 1", True, col1)
        p1_val=self.font_name.render(f"{self.player1}", True, col1)
        p2_label=self.font_name.render("PLAYER 2", True, col2)
        p2_val=self.font_name.render(f"{self.player2}", True, col2)
        screen.blit(p1_label, (50, 35))
        screen.blit(p1_val, (50, 60))
        screen.blit(p2_label, (900-180, 35))
        screen.blit(p2_val, (900-180, 60))


        back_rect=pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(0,680,110,40)

        back_hover=back_rect.collidepoint(mouse_pos)
        back_color=YELLOW if back_hover else WHITE
        back_txt=self.font_small.render("BACK", True, back_color)
        screen.blit(back_txt, (900-120, 750-50))
        
        reset_hover=reset_rect.collidepoint(mouse_pos)
        reset_color=YELLOW if reset_hover else WHITE
        reset_txt=self.font_small.render("RESET", True, reset_color)
        screen.blit(reset_txt, (30, 700))

    def execution(self):

        back_rect=pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(0,680,100,50)

        pygame.display.set_caption("Othello")
        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(64).reshape((8,8))
        self.board[3,3],self.board[4,4],self.board[3,4],self.board[4,3] = 1,1,2,2

        FPS = pygame.time.Clock()

        switch = False
        end_time=None
        game_on = True
        while True:
            FPS.tick(60)
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
                    switch = False
                    mouse_pos=pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        return 0
                    if reset_rect.collidepoint(mouse_pos):
                        self.board = np.zeros(64).reshape((8,8))
                        self.board[3,3],self.board[4,4],self.board[3,4],self.board[4,3] = 1,1,2,2
                        self.active = 1
                        self.n_active = 2
                    position = event.pos
                    box = self.box(position)
                    if ( box[0]!=-1 ):
                        valid_moves = self.valid_left()
                        if (valid_moves == False):
                            self.switch()
                            switch = True
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
            mouse_pos=pygame.mouse.get_pos()
            self.show(display,mouse_pos)
            for i in range(1,8):
                pygame.draw.line(display,GREEN,(210,170+60*i),(690,170+60*i),3)
                pygame.draw.line(display,GREEN,(210+60*i,170), (210+60*i,650),3)
            for i in range(8):
                for j in range(8):
                    if self.board[j,i] == 1:
                        pygame.draw.circle(display, col1, (215+25+60*i,175+25+60*j),25)
                    elif self.board[j,i] == 2:
                        pygame.draw.circle(display, col2, (215+25+60*i,175+25+60*j),25)
                    elif self.board[j,i] ==0 and self.finding_valid((j,i),check = True):
                        pygame.draw.circle(display, WHITE, (215+25+60*i,175+25+60*j),25)
                        pygame.draw.circle(display, BLACK, (215+25+60*i,175+25+60*j),24)
            
            score_str1 = f"{np.sum(self.board == 1)}"
            score_surf1 = self.font_big.render(score_str1, True, col1)
            score_str2 = f"{np.sum(self.board == 2)}"
            score_surf2 = self.font_big.render(score_str2, True, col2)
            display.blit(score_surf1, (35,375-200))
            display.blit(score_surf2,(770+15,375-200))

            valid_moves = self.valid_left()
            if (valid_moves == False):
                self.switch()
                switch = True
            if game_on and switch :
                no_moves = self.player1 if self.n_active == 1 else self.player2
                font = pygame.font.SysFont(None, 72)
                text = self.font_small.render(f"No valid moves for {no_moves}!", True, col1 if self.active == 2 else col2)
                rect = text.get_rect(center=(450, 80))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40), 5)
                display.blit(text, rect)
                switch = False
             
            if not game_on and time.time()-end_time>0.75:
                font = pygame.font.SysFont(None, 72)
                wincol = (255,255,255)
                if win != 0:
                    text = self.font_medium.render(f"{self.winner} Wins!", True, wincol)
                else:
                    text = self.font_medium.render("It's a Draw!", True, wincol)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40), 5)
                display.blit(text, rect)
                if not game_on and time.time()-end_time>2.5:
                    return self.winner
    
            pygame.display.update()
# play = othello(1,2)
# play.execution()
