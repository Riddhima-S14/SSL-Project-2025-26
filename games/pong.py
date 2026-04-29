from game import games_class
import pygame
import numpy as np
import os
import sys
import time
from pygame.locals import *

pygame.init()

#colors
WHITE=(255,255,255)
YELLOW=(255,255,0)
BLACK=(0,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

class Pong(games_class):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.WIDTH, self.HEIGHT=900, 750
        self.BOARD_WIDTH=838
        self.BOARD_HEIGHT=550
        self.BOARD_X=30
        self.BOARD_Y=120


        #ball knowledge
        BALL_SIZE=20

        #paddles
        PADDLE_WIDTH, PADDLE_HEIGHT=20, 120
        self.paddle_speed=8
        self.paddle1=pygame.Rect(self.BOARD_X+20, self.BOARD_Y+self.BOARD_HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2=pygame.Rect(self.BOARD_X+self.BOARD_WIDTH-40, self.BOARD_Y+self.BOARD_HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

        self.ball=pygame.Rect(self.BOARD_X+self.BOARD_WIDTH//2-BALL_SIZE//2, self.BOARD_Y+self.BOARD_HEIGHT//2-BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.ball_speed_x=6*np.random.choice([1,-1])
        self.ball_speed_y=6*np.random.choice([1,-1])

        self.score1=0
        self.score2=0
        self.winner=None

        BASE_PATH=os.path.dirname(__file__)
        ASSETS_DIR=os.path.join(BASE_PATH, '../assets')
        self.bg=pygame.image.load(os.path.join(ASSETS_DIR, "pong_bg.png")).convert()

        #fonts
        font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
        self.font_big=pygame.font.Font(font_path, 32)
        self.font_medium=pygame.font.Font(font_path, 26)
        self.font_small=pygame.font.Font(font_path, 18)
        self.font_name=pygame.font.Font(font_path, 14)

        self.back_rect=pygame.Rect(750, 680, 100, 40)
        self.reset_rect=pygame.Rect(30, 680, 100, 40)
        
    def reset_ball(self):
        self.ball.center=(self.BOARD_X+self.BOARD_WIDTH//2, self.BOARD_Y+self.BOARD_HEIGHT//2) 
        pygame.time.delay(1000)
        self.ball_speed_x=6*np.random.choice([1,-1])
        self.ball_speed_y=6*np.random.choice([1,-1])
        #speed cap
        max_speed = 15
        self.ball_speed_x = max(-max_speed, min(max_speed, self.ball_speed_x))
        self.ball_speed_y = max(-max_speed, min(max_speed, self.ball_speed_y))


    def win_check(self):
        WIN_SCORE=5
        if self.score1>=WIN_SCORE:
            return self.player1
        elif self.score2>=WIN_SCORE:
            return self.player2
        return 0

    def draw(self):
        self.display.blit(self.bg, (0, 0))

        #player labels
        p1_label=self.font_name.render("PLAYER 1", True, WHITE)
        p1_val=self.font_name.render(self.player1, True, WHITE)
        p2_label=self.font_name.render("PLAYER 2", True, WHITE)
        p2_val=self.font_name.render(self.player2, True, WHITE)
        self.display.blit(p1_label, (50, 35))
        self.display.blit(p1_val, (50, 60))
        self.display.blit(p2_label, (self.WIDTH-180, 35))
        self.display.blit(p2_val, (self.WIDTH-180, 60))

        #paddles
        pygame.draw.rect(self.display, GREEN, self.paddle1)
        pygame.draw.rect(self.display, BLUE, self.paddle2)

        #ball
        pygame.draw.ellipse(self.display, WHITE, self.ball)

        #scores
        score_text=self.font_big.render(f"{self.score1}   {self.score2}", True, WHITE)
        rect=score_text.get_rect(center=(self.WIDTH//2, 160))
        self.display.blit(score_text, rect)

        #for the buttons
        mouse_pos=pygame.mouse.get_pos()

        #back button
        back_hover=self.back_rect.collidepoint(mouse_pos)
        back_color=YELLOW if back_hover else WHITE
        back_txt=self.font_small.render("BACK", True, back_color)
        self.display.blit(back_txt, (self.WIDTH-120, self.HEIGHT-50))

        #reset button
        reset_hover=self.reset_rect.collidepoint(mouse_pos)
        reset_color=YELLOW if reset_hover else WHITE
        reset_txt=self.font_small.render("RESET", True, reset_color)
        self.display.blit(reset_txt, (40, self.HEIGHT-50))


    
    def execution(self):        
        FPS=pygame.time.Clock()
        end_time=None 
        
        self.display=pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        game_on=True

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    #back button
                    if self.back_rect.collidepoint(mouse_pos):
                        return 0
                    #reset button
                    if self.reset_rect.collidepoint(mouse_pos):
                        #reset scores, paddles, ball
                        self.score1=0
                        self.score2=0
                        self.winner=None
                        self.paddle1.y=self.BOARD_Y+self.BOARD_HEIGHT//2-60
                        self.paddle2.y=self.BOARD_Y+self.BOARD_HEIGHT//2-60
                        self.reset_ball()

                elif not game_on and event.type==KEYDOWN:
                    pygame.quit()
                    sys.exit()

            if game_on and not self.winner:
                keys=pygame.key.get_pressed()
                #player 1 controls
                if keys[K_w] and self.paddle1.top>self.BOARD_Y:
                    self.paddle1.y-=self.paddle_speed
                if keys[K_s] and self.paddle1.bottom<self.BOARD_Y+self.BOARD_HEIGHT:
                    self.paddle1.y+=self.paddle_speed
                #player 2 controls
                if keys[K_UP] and self.paddle2.top>self.BOARD_Y:
                    self.paddle2.y-=self.paddle_speed
                if keys[K_DOWN] and self.paddle2.bottom<self.BOARD_Y+self.BOARD_HEIGHT:
                    self.paddle2.y+=self.paddle_speed

                #ball movement
                self.ball.x+=self.ball_speed_x
                self.ball.y+=self.ball_speed_y

                #bounce off top/bottom
                if self.ball.top<=self.BOARD_Y:
                    self.ball.top=self.BOARD_Y
                    self.ball_speed_y*=-1
                elif self.ball.bottom>=self.BOARD_Y+self.BOARD_HEIGHT:
                    self.ball.bottom=self.BOARD_Y+self.BOARD_HEIGHT
                    self.ball_speed_y*=-1

                #elite ball knowledge
                #paddle collisions with reflected angle
                if self.ball.colliderect(self.paddle1):
                    self.ball_speed_x=abs(self.ball_speed_x)
                    #check how far it is from the center
                    offset=(self.ball.centery-self.paddle1.centery)/(self.paddle1.height//2)
                    #the further it is the faster it goes
                    self.ball_speed_y=offset*6
                    self.ball_speed_x*=1.05
                    self.ball_speed_y*=1.05
                    #speed cap
                    max_speed = 15
                    self.ball_speed_x = max(-max_speed, min(max_speed, self.ball_speed_x))
                    self.ball_speed_y = max(-max_speed, min(max_speed, self.ball_speed_y))


                if self.ball.colliderect(self.paddle2):
                    self.ball_speed_x=-abs(self.ball_speed_x)
                    offset=(self.ball.centery-self.paddle2.centery)/(self.paddle2.height//2)
                    self.ball_speed_y=offset*6
                    self.ball_speed_x*=1.05
                    self.ball_speed_y*=1.05
                    #speed cap
                    max_speed = 15
                    self.ball_speed_x = max(-max_speed, min(max_speed, self.ball_speed_x))
                    self.ball_speed_y = max(-max_speed, min(max_speed, self.ball_speed_y))


                #scoring
                if self.ball.left<=self.BOARD_X:
                    self.score2+= 1
                    self.reset_ball()
                if self.ball.right>=self.BOARD_X+self.BOARD_WIDTH:
                    self.score1+= 1
                    self.reset_ball()
                

                #win check
                winner=self.win_check()
                if winner:
                    self.winner=winner
                    end_time=time.time()
                    game_on=False

            self.draw()

            if not game_on and time.time()-end_time>0.75:
                font = pygame.font.SysFont(None, 72)
                
                text = self.font_big.render(f"{self.winner} Wins!", True, WHITE)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(self.display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(self.display, WHITE , rect.inflate(40, 40), 5)
                self.display.blit(text, rect)
                if not game_on and time.time()-end_time>2.5:
                    return self.winner
            

            pygame.display.update()

            FPS.tick(60)


# play=Pong(1,2)
# play.execution()
