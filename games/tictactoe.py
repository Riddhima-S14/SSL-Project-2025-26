from game import games_class
import numpy as np
import time
import os
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
YELLOW=(255, 255, 0)
BLUEDIM = (0,0,128)
REDDIM = (128,0,0)

class Tictactoe(games_class):
    def occ(self,x,y):
        if self.board[x,y] == 0:
            return False
        else:
            return True
    def box(self,posn):
        if posn[0]<100 or posn[0]>800 or posn[1]<25 or posn[1]>725 :
            return((-1,-1))
        else:
            x = (posn[0]-205)//49
            y = (posn[1]-165)//49
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
            self.win_line = ((205+24+posn[1][0]*49,24+165+posn[0][0]*49),(4*49+205+24+posn[1][0]*49,165+24+posn[0][0]*49))
            return self.active
        #for vertical
        v = t[0:0+length+1,:] & t[1:2+length,:] & t[2:3+length,:] & t[3:length+4,:] & t[4:length+5,:]
        if np.any(v):
            posn = np.where(v ==1) 
            self.win_line = ((205+24+int(posn[1][0])*49,165+24+int(posn[0][0])*49),(205+24+int(posn[1][0])*49,4*49+165+24+int(posn[0][0])*49))        
            return self.active
        #top left to bottom right diagonal
        d1 = t[0:0+length+1,0:0+length+1] &   t[1:2+length,1:2+length] & t[2:3+length,2:3+length] & t[3:length+4,3:length+4] & t[4:length+5,4:length+5]
        if np.any(d1):
            posn = np.where(d1 == 1)
            self.win_line = ((205+24+posn[1][0]*49,165+24+posn[0][0]*49),(4*49+205+24+posn[1][0]*49,4*49+165+24+posn[0][0]*49))
            return self.active
        #bottom left to top right
        d2 = t[rows-1-length:rows,0:0+length+1] & t[rows-length-2:rows-1,1:2+length] & t[rows-length-3:rows-2,2:3+length] & t[rows-length-4:rows-3,3:length+4] & t[rows-length-5:rows-4,4:length+5]
        if np.any(d2):
            posn = np.where(d2 == 1)
            self.win_line = ((205+24+(posn[1][0])*49,165+24+(posn[0][0]+4)*49),(4*49+205+24+posn[1][0]*49,165+24+(posn[0][0]+4)*49-4*49))
            return self.active
        return 0 
    def draw_cross(self,surface, color, center_pos, size):
        x, y = center_pos
        pygame.draw.line(surface, color, (x - size+5, y - size), (x + size-5, y + size),5)
        pygame.draw.line(surface, color, (x + size-5, y - size), (x - size+5, y + size),5)
    def show(self,screen, mouse_pos):
        BASE_PATH=os.path.dirname(__file__)
        ASSETS_DIR=os.path.join(BASE_PATH, 'assets')

        font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
        font_big=pygame.font.Font(font_path, 50)
        font_medium=pygame.font.Font(font_path, 26)
        font_small=pygame.font.Font(font_path, 18)
        font_name=pygame.font.Font(font_path, 18)

        bg_main=pygame.image.load(os.path.join(ASSETS_DIR, "Tictactoe_image.jpeg")).convert()
        screen.blit(bg_main, (0, 0))

        p1_label=font_name.render("PLAYER 1", True, WHITE)
        p1_symbol = font_big.render("O",True,BLUE)
        p1_val=font_name.render(f"{self.player1}", True, WHITE)
        p2_label=font_name.render("PLAYER 2", True, WHITE)
        p2_symbol = font_big.render("X",True,RED)
        p2_val=font_name.render(f"{self.player2}", True, WHITE)
        screen.blit(p1_label, (50, 35))
        screen.blit(p1_val, (50, 60))
        screen.blit(p1_symbol, (60,120))
        screen.blit(p2_label, (900-160, 35))
        screen.blit(p2_val, (900-160, 60))
        screen.blit(p2_symbol, (900-110,120))


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
        FPS = pygame.time.Clock()
        FPS.tick(60)

        back_rect=pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(0,680,100,50)

        display = pygame.display.set_mode((900,750))
        self.board = np.zeros(100).reshape((10,10))
        pygame.display.set_caption("Tic Tac Toe")
        game_on=True
        while True:
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        return 0
                    if reset_rect.collidepoint(mouse_pos):
                        self.board = np.zeros(100).reshape((10,10))
                        self.active = 1
                    position = event.pos
                    g_box = self.box(position)
                    if (g_box[0] >= 0):
                        if (self.occ(g_box[0],g_box[1]) == False):
                            self.board[g_box[0],g_box[1]] = self.active
                            winner=self.win_check()                     
                            if winner!=0:
                                self.winner= self.player1 if self.active == 1 else self.player2
                                end_time=time.time()
                                game_on=False
                            elif not np.any(self.board == 0):
                        #draw
                                end_time=time.time()
                                game_on=False
                            else:
                                self.switch()


            mouse_pos=pygame.mouse.get_pos()
            self.show(display,mouse_pos)


            for i in range(0,11):
                pygame.draw.line(display,GREEN,(205,165+49*i),(695,165+49*i),3)
                pygame.draw.line(display,GREEN,(205+49*i,165), (205+49*i,655),3)
            for i in range(10):
                for j in range(10):
                    if self.board[j,i] == 0:
                        hover_zone = pygame.Rect(205+49*i,165+49*j,49,49)
                        if hover_zone.collidepoint(mouse_pos):
                            if self.active == 1:
                                pygame.draw.circle(display, BLUEDIM, (205+24+49*i,165+24+49*j), 20)
                                pygame.draw.circle(display, BLACK, (205+24+49*i,165+24+49*j), 17)
                            else:
                                self.draw_cross(display,REDDIM,(205+24+49*i,165+24+49*j),20)   
                    elif self.board[j,i] == 1:
                        pygame.draw.circle(display, BLUE, (205+24+49*i,165+24+49*j), 20)
                        pygame.draw.circle(display, BLACK, (205+24+49*i,165+24+49*j), 17)

                    elif self.board[j,i] == 2:
                        self.draw_cross(display,RED,(205+24+49*i,165+24+49*j),20)
            if not game_on and self.win_line:
                pygame.draw.line(display, WHITE, self.win_line[0], self.win_line[1], 8)
            if not game_on and time.time()-end_time>1.25:
                BASE_PATH=os.path.dirname(__file__)
                ASSETS_DIR=os.path.join(BASE_PATH, 'assets')

                font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
                font_end=pygame.font.Font(font_path, 72)
                col =  BLUE if self.winner == 1 else RED
                if self.winner != 0:
                    text = font_end.render(f" {self.winner} Wins!", True, col)
                else:
                    text = font_end.render("It's a Draw!", True, GREEN)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, GREEN if self.winner == 0 else col, rect.inflate(40, 40), 5)
                display.blit(text, rect)
                if not game_on and time.time()-end_time>2.5:
                    return self.winner        
            pygame.display.update()    

# play = Tictactoe(1,2)
# play.execution()
