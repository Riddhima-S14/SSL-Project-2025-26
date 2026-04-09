from game import games
import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT=900, 750
display=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

#colors
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

FPS=pygame.time.Clock()
FPS.tick(60)
end_time=None

#paddle
PADDLE_WIDTH, PADDLE_HEIGHT=20, 120
paddle_speed=8

#ball knowledge
BALL_SIZE=20

font=pygame.font.SysFont(None, 72)

#win conditions
WIN_SCORE=5


class Pong(games):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.paddle1=pygame.Rect(50, HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle2=pygame.Rect(WIDTH-70, HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball=pygame.Rect(WIDTH//2-BALL_SIZE//2, HEIGHT//2-BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        self.ball_speed_x=6*random.choice((1,-1))
        self.ball_speed_y=6*random.choice((1,-1))
        self.score1=0
        self.score2=0
        self.winner=None

    def reset_ball(self):
        self.ball.center=(WIDTH//2, HEIGHT//2)
        draw(self)
        pygame.display.update()
        pygame.time.delay(1000)
        self.ball_speed_x=6*random.choice((1,-1))
        self.ball_speed_y=6*random.choice((1,-1))

    def win_check(self):
        if self.score1>=WIN_SCORE:
            return self.player1
        elif self.score2>=WIN_SCORE:
            return self.player2
        return 0


def draw(play):
    display.fill(BLACK)
    #paddles
    pygame.draw.rect(display, GREEN, play.paddle1)
    pygame.draw.rect(display, BLUE, play.paddle2)
    #ball
    pygame.draw.ellipse(display, WHITE, play.ball)
    #scores
    score_text=font.render(f"{play.score1}   {play.score2}", True, WHITE)
    rect=score_text.get_rect(center=(WIDTH//2, 50))
    display.blit(score_text, rect)
    #Winner message
    if play.winner:
        win_text=font.render(f"Player {play.winner} Wins!", True, WHITE)
        rect2=win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(display, BLACK, rect2.inflate(40,40))
        pygame.draw.rect(display, WHITE, rect2.inflate(40,40), 5)
        display.blit(win_text, rect2)
    pygame.display.update()


play=Pong(1,2)
game_on=True

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif not game_on and event.type==KEYDOWN:
            pygame.quit()
            sys.exit()

    if game_on and not play.winner:
        keys=pygame.key.get_pressed()
        #player 1 controls
        if keys[K_w] and play.paddle1.top>0:
            play.paddle1.y-=paddle_speed
        if keys[K_s] and play.paddle1.bottom<HEIGHT:
            play.paddle1.y+=paddle_speed
        #player 2 controls
        if keys[K_UP] and play.paddle2.top>0:
            play.paddle2.y-=paddle_speed
        if keys[K_DOWN] and play.paddle2.bottom<HEIGHT:
            play.paddle2.y+=paddle_speed

        #ball movement
        play.ball.x+=play.ball_speed_x
        play.ball.y+=play.ball_speed_y

        #bounce off top/bottom
        if play.ball.top<=0:
            play.ball.top=0
            play.ball_speed_y*=-1
        elif play.ball.bottom>=HEIGHT:
            play.ball.bottom=HEIGHT
            play.ball_speed_y*=-1

        #paddle collisions with reflected angle
        if play.ball.colliderect(play.paddle1):
            play.ball_speed_x=abs(play.ball_speed_x)
            offset=(play.ball.centery-play.paddle1.centery)/(PADDLE_HEIGHT//2)
            play.ball_speed_y=offset*6
            play.ball_speed_x*=1.05
            play.ball_speed_y*=1.05



        if play.ball.colliderect(play.paddle2):
            play.ball_speed_x=-abs(play.ball_speed_x)
            offset=(play.ball.centery-play.paddle2.centery)/(PADDLE_HEIGHT//2)
            play.ball_speed_y=offset*6
            play.ball_speed_x*=1.05
            play.ball_speed_y*=1.05
            #speed cap
            max_speed = 15
            play.ball_speed_x = max(-max_speed, min(max_speed, play.ball_speed_x))
            play.ball_speed_y = max(-max_speed, min(max_speed, play.ball_speed_y))


        #scoring
        if play.ball.left<=0:
            play.score2+= 1
            play.reset_ball()
        if play.ball.right>=WIDTH:
            play.score1+= 1
            play.reset_ball()
            #speed cap
            max_speed = 15
            play.ball_speed_x = max(-max_speed, min(max_speed, play.ball_speed_x))
            play.ball_speed_y = max(-max_speed, min(max_speed, play.ball_speed_y))


        #win check
        winner=play.win_check()
        if winner:
            play.winner=winner
            end_time=time.time()
            game_on=False

    draw(play)
    FPS.tick(60)