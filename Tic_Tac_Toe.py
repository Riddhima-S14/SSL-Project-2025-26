from game import games
import numpy as np
import pygame
import time
from pygame.locals import *
pygame.init()

#player 1 - circle - 1
#player 2 - cross - 2 
display = pygame.display.set_mode((900,750))
board = np.zeros(100).reshape((10,10))
#colors

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
FPS = pygame.time.Clock()
FPS.tick(60)

#drawing

def draw_cross(surface, color, center_pos, size):
    x, y = center_pos
    pygame.draw.line(surface, color, (x - size+5, y - size), (x + size-5, y + size),5)
    pygame.draw.line(surface, color, (x + size-5, y - size), (x - size+5, y + size),5)


class Tictactoe(games):
    def win_check(self):
        pass
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
            

pygame.display.set_caption("Tic Tac Toe")

def end_message(text, seconds):
    display.fill((251,72,196)) 
    change_font = pygame.font.SysFont("Times New Roman", 60,bold=True)
    message_surface = change_font.render(text, True, (0, 0, 0)) 
    #pygame.draw.rect(display, (0, 0, 0), (375, 375, , 50))
    rect = message_surface.get_rect(center=(450, 375))
    display.blit(message_surface, rect)
    
    pygame.display.flip() 
    time.sleep(seconds)     
            

play = Tictactoe(1,2,board)

while True:
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
            g_box = play.box(position)
            if (g_box[0] > 0):
                if (play.occ(g_box[0],g_box[1]) == False):
                    play.board[g_box[0],g_box[1]] = play.active
                    winner=play.win_check()                     
                    if winner!=0:
                        play.winner=play.active
                        text = f"Player {play.active} Wins!"
                        end_message(text,2)
                        game_on=False
                    elif not np.any(play.board == 0):
                        #draw
                        end_message("Its a Draw!",2)
                        game_on=False
                    else:
                        play.switch()

    display.fill(BLACK)
    for i in range(1,10):
        pygame.draw.line(display,GREEN,(100,25+70*i),(800,25+70*i),3)
        pygame.draw.line(display,GREEN,(100+70*i,25), (100+70*i,725),3)
    for i in range(10):
        for j in range(10):
            if play.board[j,i] == 1:
                pygame.draw.circle(display, BLUE, (135+70*i,60+70*j), 25)
                pygame.draw.circle(display, BLACK, (135+70*i,60+70*j), 20)

            elif play.board[j,i] == 2:
                draw_cross(display,RED,(135+70*i,60+70*j),25)
    
    pygame.display.update()