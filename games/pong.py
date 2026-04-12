from game import games
import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

#colors
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

class Pong(games):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        WIDTH, HEIGHT=900, 750
        #ball knowledge
        BALL_SIZE=20
        #paddle
        PADDLE_WIDTH, PADDLE_HEIGHT=20, 120
        self.paddle_speed=8
        self.paddle1=pygame.Rect(50, HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2=pygame.Rect(WIDTH-70, HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball=pygame.Rect(WIDTH//2-BALL_SIZE//2, HEIGHT//2-BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.ball_speed_x=6*random.choice((1,-1))
        self.ball_speed_y=6*random.choice((1,-1))
        self.score1=0
        self.score2=0
        self.winner=None

    def reset_ball(self):
        self.ball.center=(900//2, 750//2) #width,height //2
        self.draw(self,900,750) #(self,WIDTH,HEIGHT)
        pygame.display.update()
        pygame.time.delay(1000)
        self.ball_speed_x=6*random.choice((1,-1))
        self.ball_speed_y=6*random.choice((1,-1))

    def win_check(self):
        WIN_SCORE=5
        if self.score1>=WIN_SCORE:
            return self.player1
        elif self.score2>=WIN_SCORE:
            return self.player2
        return 0

    def draw(self,play,WIDTH,HEIGHT):
        font=pygame.font.SysFont(None, 72)
        self.display.fill(BLACK)
    #paddles
        pygame.draw.rect(self.display, GREEN, self.paddle1)
        pygame.draw.rect(self.display, BLUE, self.paddle2)
    #ball
        pygame.draw.ellipse(self.display, WHITE, self.ball)
    #scores
        score_text=font.render(f"{play.score1}   {play.score2}", True, WHITE)
        rect=score_text.get_rect(center=(WIDTH//2, 50))
        self.display.blit(score_text, rect)
    #Winner message
        if self.winner:
            win_text=font.render(f"Player {play.winner} Wins!", True, WHITE)
            rect2=win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            pygame.draw.rect(self.display, BLACK, rect2.inflate(40,40))
            pygame.draw.rect(self.display, WHITE, rect2.inflate(40,40), 5)
            self.display.blit(win_text, rect2)
        pygame.display.update()
    def execution(self):        
        FPS=pygame.time.Clock()
        FPS.tick(60)
        end_time=None 
        #design
        WIDTH, HEIGHT=900, 750
        #ball knowledge
        BALL_SIZE=20
        #paddle
        PADDLE_WIDTH, PADDLE_HEIGHT=20, 120
        self.display=pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        game_on=True

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                elif not game_on and event.type==KEYDOWN:
                    pygame.quit()
                    sys.exit()

            if game_on and not self.winner:
                keys=pygame.key.get_pressed()
        #player 1 controls
                if keys[K_w] and self.paddle1.top>0:
                    self.paddle1.y-=self.paddle_speed
                if keys[K_s] and self.paddle1.bottom<HEIGHT:
                    self.paddle1.y+=self.paddle_speed
        #player 2 controls
                if keys[K_UP] and self.paddle2.top>0:
                    self.paddle2.y-=self.paddle_speed
                if keys[K_DOWN] and self.paddle2.bottom<HEIGHT:
                    self.paddle2.y+=self.paddle_speed

        #ball movement
                self.ball.x+=self.ball_speed_x
                self.ball.y+=self.ball_speed_y

                #bounce off top/bottom
                if self.ball.top<=0:
                    self.ball.top=0
                    self.ball_speed_y*=-1
                elif self.ball.bottom>=HEIGHT:
                    self.ball.bottom=HEIGHT
                    self.ball_speed_y*=-1

        #paddle collisions with reflected angle
                if self.ball.colliderect(self.paddle1):
                    self.ball_speed_x=abs(self.ball_speed_x)
                    offset=(self.ball.centery-self.paddle1.centery)/(PADDLE_HEIGHT//2)
                    self.ball_speed_y=offset*6
                    self.ball_speed_x*=1.05
                    self.ball_speed_y*=1.05



                if self.ball.colliderect(self.paddle2):
                    self.ball_speed_x=-abs(self.ball_speed_x)
                    offset=(self.ball.centery-self.paddle2.centery)/(PADDLE_HEIGHT//2)
                    self.ball_speed_y=offset*6
                    self.ball_speed_x*=1.05
                    self.ball_speed_y*=1.05
            #speed cap
                    max_speed = 15
                    self.ball_speed_x = max(-max_speed, min(max_speed, self.ball_speed_x))
                    self.ball_speed_y = max(-max_speed, min(max_speed, self.ball_speed_y))


        #scoring
                if self.ball.left<=0:
                    self.score2+= 1
                    self.reset_ball()
                if self.ball.right>=WIDTH:
                    self.score1+= 1
                    self.reset_ball()
            #speed cap
                    max_speed = 15
                    self.ball_speed_x = max(-max_speed, min(max_speed, self.ball_speed_x))
                    self.ball_speed_y = max(-max_speed, min(max_speed, self.ball_speed_y))


        #win check
                winner=self.win_check()
                if winner:
                    self.winner=winner
                    end_time=time.time()
                    game_on=False
                if not game_on and time.time()-end_time > 1.25:
                    font=pygame.font.SysFont(None, 72)
                    if self.winner !=0 :
                        text=font.render(f"Player {self.winner} Wins!", True, GREEN)

                    rect=text.get_rect(center=(450, 375))
                    pygame.draw.rect(self.display, BLACK, rect.inflate(40, 40))
                    pygame.draw.rect(self.display, GREEN, rect.inflate(40, 40), 5)
                    self.display.blit(text, rect)

            self.draw(self,WIDTH,HEIGHT)
            FPS.tick(60)


# play=Pong(1,2)
# play.execution()
