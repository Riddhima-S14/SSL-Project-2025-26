from game import games_class
import numpy as np
import pygame
import os
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
WHITE = (255, 255, 255)
YELLOW=(255, 255, 0)

FPS = pygame.time.Clock()
FPS.tick(60)
end_time=None

class Connect(games_class):
    def occ(self,x,y):
        if (self.board[x,y] == 0 ):
            return False
        else:
            return True
    def column(self,pos):
        if pos[0]>=205 and pos[0]<205+490 :
            column = (pos[0]-205)//70
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
    def show(self,screen, mouse_pos):
        BASE_PATH=os.path.dirname(__file__)
        ASSETS_DIR=os.path.join(BASE_PATH, 'assets')

        font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
        font_big=pygame.font.Font(font_path, 50)
        font_medium=pygame.font.Font(font_path, 26)
        font_small=pygame.font.Font(font_path, 18)
        font_name=pygame.font.Font(font_path, 18)

        bg_main=pygame.image.load(os.path.join(ASSETS_DIR, "Connect4_image.jpeg")).convert()
        screen.blit(bg_main, (0, 0))

        p1_label=font_name.render("PLAYER 1", True, col1)
        p1_val=font_name.render(f"{self.player1}", True, col1)
        p2_label=font_name.render("PLAYER 2", True, col2)
        p2_val=font_name.render(f"{self.player2}", True, col2)
        screen.blit(p1_label, (50, 35))
        screen.blit(p1_val, (50, 60))
        screen.blit(p2_label, (900-180, 35))
        screen.blit(p2_val, (900-180, 60))

        back_rect=pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(0,680,110,40)

        back_hover=back_rect.collidepoint(mouse_pos)
        back_color=YELLOW if back_hover else WHITE
        back_txt=font_small.render("BACK", True, back_color)
        screen.blit(back_txt, (900-120, 750-50))

        reset_hover=reset_rect.collidepoint(mouse_pos)
        reset_color=YELLOW if reset_hover else WHITE
        reset_txt=font_small.render("RESET", True, reset_color)
        screen.blit(reset_txt, (30, 700))

    def execution(self):
        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(49).reshape((7,7))
        FPS = pygame.time.Clock()
        FPS.tick(60)
        end_time=None
        pygame.display.set_caption("Connect 4")
        game_on = True
        back_rect=pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(0,680,110,40)
        
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos
                    mouse_pos=pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        return 0
                    if reset_rect.collidepoint(mouse_pos):
                        self.board = np.zeros(49).reshape((7,7))
                        self.active = 1
                    c = self.column(position)
                    if c >= 0 :
                        row = self.available_row(c)
                        if row >= 0:
                            self.board[row,c] = self.active
                            winner= self.win_check()                     
                            if winner!=0:
                                self.winner=self.player1 if self.active == 1 else self.player2
                                end_time=time.time()
                                game_on=False
                            elif not np.any(self.board == 0):
                                #draw
                                end_time=time.time()
                                game_on=False
                            else:
                                self.switch()
                elif not game_on and time.time()-end_time>2.5:
                    return 0
            mouse_pos=pygame.mouse.get_pos()
            self.show(display,mouse_pos)
            pygame.draw.rect(display, boardcol, (205,165,490,490))
        
            for r in range(7):
                for c in range(7):
                    if self.board[r,c] == 1 :
                        pygame.draw.circle(display, col1 , (240+70*(c),200 + 70*(r)), 25)
                    elif self.board[r,c] == 2:
                        pygame.draw.circle(display, col2 , (240+70*(c),200 + 70*(r)), 25)
                    elif self.board[r,c] == -1:
                        pygame.draw.circle(display, win , (240+70*(c),200 + 70*(r)), 25)
                    elif self.board[r,c] == 0:
                        pygame.draw.circle(display, BLACK , (240+70*(c),200 + 70*(r)), 25)
    
            if not game_on and time.time()-end_time>1.25:
                font = pygame.font.SysFont(None, 72)
                if self.winner != 0:
                    text = font.render(f"{self.winner} Wins!", True, win)
                else:
                    text = font.render("It's a Draw!", True, win)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, win , rect.inflate(40, 40), 5)
                display.blit(text, rect)
    
            pygame.display.update()
# play = Connect(1,2)
# play.execution()
