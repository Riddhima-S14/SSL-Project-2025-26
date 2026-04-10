#othello
from game import games
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()

display = pygame.display.set_mode((900,750))
board = np.zeros(64).reshape((8,8))
board[3,3],board[4,4],board[3,4],board[4,3] = 1,1,2,2

#player 1 - 1 - col 1
#player 2 - 2 - col 2

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
boardcol = (0,236,255)
col1 = (103,21,255)
col2 = (255,0,127)
wincol = (255,136,0)

FPS = pygame.time.Clock()

end_time=None

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
        
    def is_valid_coord(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def finding_valid(self, box, check=False):
        if self.board[box] != 0:
            return False

        valid_direction = False
        directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

        for dr, dc in directions:
            r, c = box[0] + dr, box[1] + dc
            pieces_to_flip = []

            while self.is_valid_coord(r, c) and self.board[r, c] == self.n_active:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if self.is_valid_coord(r, c) and self.board[r, c] == self.active and pieces_to_flip:
                if check: 
                    return True 

                valid_direction = True
                self.board[box] = self.active 
                for fr, fc in pieces_to_flip:
                    self.board[fr, fc] = self.active

        return valid_direction

    def valid_left(self):
        for i in range(8):
            for j in range(8):
                if self.finding_valid((i, j),True):
                    return True
        return False
    def win_check(self):
        score1 = np.sum(self.board == 1)
        score2 = np.sum(self.board == 2)
        if score1 > score2:
            return 1
        elif score2 > score1:
            return 2
        return 0
    
pygame.display.set_caption("Othello")

play = othello(1,2,board)
game_on = True

while True:
    FPS.tick(60)
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
        elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            box = play.box(position)
            if ( box[0]!=-1 ):
                valid_moves = play.valid_left()
                if (valid_moves == False):
                    play.switch()
                    if(play.valid_left() == False ):
                        win = play.win_check()
                        if win!=0:
                            play.winner = win
                            end_time=time.time()
                            game_on=False
                        else:
                            end_time=time.time()
                            game_on=False
                else:
                    move = play.finding_valid(box)
                    if(move):
                        if (np.any(play.board == 0) == False):
                            win = play.win_check()
                            if win!=0:
                                play.winner = win
                                end_time=time.time()
                                game_on=False
                            else:
                                end_time=time.time()
                                game_on=False
                        else:
                            play.switch()
        elif not game_on and event.type == pygame.KEYDOWN:
            pygame.quit()
            exit()

    display.fill(BLACK)
    for i in range(1,8):
        pygame.draw.line(display,GREEN,(130,55+80*i),(770,55+80*i),3)
        pygame.draw.line(display,GREEN,(130+80*i,55), (130+80*i,695),3)
    for i in range(8):
        for j in range(8):
            if play.board[j,i] == 1:
                pygame.draw.circle(display, col1, (170+80*i,95+80*j),35)
            elif play.board[j,i] == 2:
                pygame.draw.circle(display, col2, (170+80*i,95+80*j),35)
    
    if not game_on and time.time()-end_time>0.75:
        font = pygame.font.SysFont(None, 72)
        if play.winner != 0:
            text = font.render(f"Player {play.winner} Wins!", True, wincol)
        else:
            text = font.render("It's a Draw!", True, wincol)
        rect = text.get_rect(center=(450, 375))
        pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
        pygame.draw.rect(display, wincol , rect.inflate(40, 40), 5)
        display.blit(text, rect)
    
    pygame.display.update()

            




            

