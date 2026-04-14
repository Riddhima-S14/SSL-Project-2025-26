import sys
import time
import pygame
import numpy as np
from games.tictactoe import Tictactoe
from games.connect4 import Connect
from games.pong import Pong
from games.battleship import Battleship

pygame.init()

WIDTH, HEIGHT=900, 750
WHITE=(255, 255, 255)
YELLOW=(255, 255, 0)
BLACK=(0, 0, 0)

#player1="s"
#player2="r"
player1=sys.argv[1]
player2=sys.argv[2]

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Arcade")

font_big=pygame.font.Font("PressStart2P-Regular.ttf", 36)
font_small=pygame.font.Font("PressStart2P-Regular.ttf", 18)
font_name=pygame.font.Font("PressStart2P-Regular.ttf", 14)
font_game=pygame.font.Font("PressStart2P-Regular.ttf", 16)

main_stars=pygame.image.load("space_arcade_stars.png")
main_no_stars=pygame.image.load("space_arcade_no_stars.png")
bg_stars=pygame.image.load("background_stars.png")
bg_no_stars=pygame.image.load("background_no_stars.png")

menu_0=pygame.image.load("menu_blue.png")
menu_1=pygame.image.load("menu_1.png")
menu_2=pygame.image.load("menu_2.png")
menu_3=pygame.image.load("menu_3.png")
menu_4=pygame.image.load("menu_4.png")
menu_5=pygame.image.load("menu_5.png")

play_rect=font_big.render("PLAY", True, WHITE).get_rect(center=(WIDTH//2, 500))
stats_rect=font_big.render("STATS", True, WHITE).get_rect(center=(WIDTH//2, 600))
back_rect=font_small.render("BACK", True, WHITE).get_rect(bottomright=(WIDTH-55, HEIGHT-45))

box1=pygame.Rect(115, 315, 200, 155)
box2=pygame.Rect(365, 315, 200, 155)
box3=pygame.Rect(610, 315, 200, 155)
box4=pygame.Rect(230, 520, 200, 160)
box5=pygame.Rect(480, 520, 200, 160)

FPS=pygame.time.Clock()
show_stars=True
last_blink=time.time()
blink_interval=0.5
state="main"


def draw_players():
    p1_text=font_small.render("PLAYER 1", True, WHITE)
    p2_text=font_small.render("PLAYER 2", True, WHITE)
    p1_name=font_name.render(player1, True, WHITE)
    p2_name=font_name.render(player2, True, WHITE)

    p1_rect=p1_text.get_rect(topleft=(50, 30))
    p2_rect=p2_text.get_rect(topright=(WIDTH - 50, 30))

    p1_name_rect=p1_name.get_rect(midtop=(p1_rect.centerx, p1_rect.bottom + 18))
    p2_name_rect=p2_name.get_rect(midtop=(p2_rect.centerx, p2_rect.bottom + 18))

    screen.blit(p1_text, p1_rect)
    screen.blit(p2_text, p2_rect)
    screen.blit(p1_name, p1_name_rect)
    screen.blit(p2_name, p2_name_rect)


def hovered_box(pos):
    if box1.collidepoint(pos):
        return 1
    if box2.collidepoint(pos):
        return 2
    if box3.collidepoint(pos):
        return 3
    if box4.collidepoint(pos):
        return 4
    if box5.collidepoint(pos):
        return 5
    return 0


def launch_game(choice):
    if choice==1:
        Tictactoe(player1, player2).execution()
    elif choice==2:
        Connect(player1, player2).execution()
    elif choice==3:
        Pong(player1, player2).execution()
    elif choice==4:
        Battleship(player1, player2, (7, 10)).execution()
    elif choice==5:
        pass

running=True
while running:
    mouse_pos=pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN:
            if state=="main":
                if play_rect.collidepoint(event.pos):
                    state="menu"
                elif stats_rect.collidepoint(event.pos):
                    pass

            elif state=="menu":
                hover=hovered_box(event.pos)

                if hover!=0:
                    launch_game(hover)
                    state="menu"

                elif back_rect.collidepoint(event.pos):
                    state="main"

    if time.time()-last_blink>blink_interval:
        show_stars=not show_stars
        last_blink=time.time()

    if show_stars:
        if state=="main":
            screen.blit(main_stars, (0, 0))
        else:
            screen.blit(bg_stars, (0, 0))
    else:
        if state=="main":
            screen.blit(main_no_stars, (0,0))
        else:
            screen.blit(bg_no_stars, (0, 0))

    draw_players()

    if state=="main":
        play_text=font_big.render("PLAY", True, YELLOW if play_rect.collidepoint(mouse_pos) else WHITE)
        stats_text=font_big.render("STATS", True, YELLOW if stats_rect.collidepoint(mouse_pos) else WHITE)

        screen.blit(play_text, play_rect)
        screen.blit(stats_text, stats_rect)

    elif state=="menu":
        hover=hovered_box(mouse_pos)

        if hover==0:
            screen.blit(menu_0, (0, 0))
        elif hover==1:
            screen.blit(menu_1, (0, 0))
        elif hover==2:
            screen.blit(menu_2, (0, 0))
        elif hover==3:
            screen.blit(menu_3, (0, 0))
        elif hover==4:
            screen.blit(menu_4, (0, 0))
        elif hover==5:
            screen.blit(menu_5, (0, 0))

        draw_players()

        title_text=font_big.render("CHOOSE YOUR GAME", True, YELLOW)
        title_rect=title_text.get_rect(center=(WIDTH // 2, 135))
        screen.blit(title_text, title_rect)

        if hover==1:
            name_text=font_game.render("TIC TAC TOE", True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 225)))
        elif hover==2:
            name_text = font_game.render("CONNECT 4", True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 225)))
        elif hover==3:
            name_text = font_game.render("PONG", True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 225)))
        elif hover==4:
            name_text = font_game.render("BATTLESHIP", True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 225)))
        elif hover==5:
            name_text = font_game.render("OTHELLO", True, WHITE)
            screen.blit(name_text, name_text.get_rect(center=(WIDTH // 2, 225)))

        back_text=font_small.render("BACK", True, YELLOW if back_rect.collidepoint(mouse_pos) else WHITE)
        screen.blit(back_text, back_rect)

    pygame.display.flip()
    FPS.tick(60)
