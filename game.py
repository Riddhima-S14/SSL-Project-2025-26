import sys
import time
import pygame
import random
import os
import numpy as np
import matplotlib.pyplot as plt

class games_class:
    def __init__(self, player1, player2, board=np.zeros(5)):
        self.player1 = player1
        self.player2 = player2
        self.active = 1
        self.n_active = 2
        self.board = board
        self.winner = None

    def switch(self):
        self.active, self.n_active = self.n_active, self.active

    def box(self, posn):
        pass

    def win_check(self):
        pass

    def display(self):
        print(self.board)

    def is_board_full(self):
        return not np.any(self.board == 0)

pygame.init()

#window setup
WIDTH, HEIGHT=900, 750
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Hub")

#colours
WHITE=(255, 255, 255)
YELLOW=(255, 255, 0)
TEAL=(0, 128, 128)

#input names

if len(sys.argv)>1:
    player1=sys.argv[1]
    player2=sys.argv[2]
else:
    player1="s"
    player2="r"

#setting up paths
BASE_PATH=os.path.dirname(__file__)
ASSETS_DIR=os.path.join(BASE_PATH, 'assets')


#fonts
font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
font_big=pygame.font.Font(font_path, 32)
font_medium=pygame.font.Font(font_path, 26)
font_small=pygame.font.Font(font_path, 18)
font_name=pygame.font.Font(font_path, 14)

#load background
bg_main=pygame.image.load(os.path.join(ASSETS_DIR, "bg_main.png")).convert()


#main screen animation
GHOST_SIZE=(45, 45)

def load_and_scale(name, size):
    path=os.path.join(ASSETS_DIR, name)
    img=pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

pac_img=load_and_scale("pac.png", GHOST_SIZE)

ghost_imgs = [
    load_and_scale("red.png", GHOST_SIZE),
    load_and_scale("teal.png", GHOST_SIZE),
    load_and_scale("pink.png", GHOST_SIZE),
    load_and_scale("orange.png", GHOST_SIZE)
]

pac_x=WIDTH
pac_y=675 
speed=8
initial_gap=120 #between pac-man and the first ghost
ghost_gap=70

#load menu images

menu_bgs=[]
menu_names=["menu_normal.png", "menu_1.png", "menu_2.png", "menu_3.png", "menu_4.png", "menu_5.png"]

for name in menu_names:
    path=os.path.join(ASSETS_DIR, name)
    menu_bgs.append(pygame.image.load(path).convert())
    
games_list=["", "TIC-TAC-TOE", "CONNECT-4", "OTHELLO", "BATTLESHIP", "PONG"]

#option boxes
box_rects = [
    pygame.Rect(130, 280, 165, 170),
    pygame.Rect(365, 280, 165, 170),
    pygame.Rect(600, 280, 165, 170),
    pygame.Rect(252, 480, 165, 170),
    pygame.Rect(490, 480, 165, 170)
]

#back rectangle
back_rect=pygame.Rect(750, 680, 100, 40)

#menu animations
crossing=False
gx=-100
gy=400
g_speed=5
gap=100
pac_dir="left"
#g_img=ghost_imgs[0]
last_exit=time.time()
g_dir="horizontal"
spawn_delay=1.0 

#variables
state="main" 
show_blink=True
last_blink=time.time()
FPS=pygame.time.Clock()


#to draw player labels and names
def draw_players():
    p1_label=font_name.render("PLAYER 1", True, WHITE)
    p1_val=font_name.render(player1, True, WHITE)
    p2_label=font_name.render("PLAYER 2", True, WHITE)
    p2_val=font_name.render(player2, True, WHITE)
    screen.blit(p1_label, (50, 35))
    screen.blit(p1_val, (50, 60))
    screen.blit(p2_label, (WIDTH-180, 35))
    screen.blit(p2_val, (WIDTH-180, 60))

#for the menu
def get_hover():
    mouse_pos=pygame.mouse.get_pos()
    for i, rect in enumerate(box_rects):
        if rect.collidepoint(mouse_pos):
            return i + 1
    return 0

winner = 0

def launch_game(choice):
    if choice==1: 
        from games.tictactoe import Tictactoe
        return Tictactoe(player1, player2).execution()
    elif choice==2:
        from games.connect4 import Connect
        return Connect(player1, player2).execution()
    elif choice==3:
        from games.othello import othello
        return othello(player1, player2).execution()
    elif choice==4: 
        from games.battleship import Battleship
        return Battleship(player1, player2, (10,7)).execution()
    elif choice==5: 
        from games.pong import Pong
        return Pong(player1, player2).execution()

def history(w,l,game):
    with open('history.csv','a') as f:
        f.write(w+','+l+','+game+'\n')


def update(winner,game):
    if not( winner == 0.5 or winner == 0):
        loser = player1 if (winner == player2) else player2
        history(winner,loser,game)
running=True
if __name__ == "__main__":
    while running:
        mouse_pos=pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False
            if event.type==pygame.KEYDOWN:
                if state=="main" and event.key==pygame.K_RETURN:
                    state="animation"
                    pac_x=WIDTH #reset the animation
        
            if event.type==pygame.MOUSEBUTTONDOWN:
                if state=="menu":
                    hover=get_hover()
                    if hover!=0:
                        winner = launch_game(hover)
                        update(winner,games_list[hover])
                        state == "menu"
                    elif back_rect.collidepoint(mouse_pos):
                        state="main"

        if time.time()-last_blink>0.5:
            show_blink=not show_blink
            last_blink=time.time()

        if state=="main":
            screen.blit(bg_main, (0, 0))
            draw_players()
            if show_blink:
                blink_txt=font_medium.render("INSERT COIN TO START", True, YELLOW)
                screen.blit(blink_txt, blink_txt.get_rect(center=(WIDTH//2, 395)))

        elif state=="animation":
            screen.blit(bg_main, (0, 0))
            draw_players()
            pac_x-=speed
            screen.blit(pac_img, (pac_x, pac_y))
            ghosts_visible=0
            for i, img in enumerate(ghost_imgs):
                gx=pac_x+initial_gap+(i*ghost_gap)
                if gx+img.get_width()>0:
                    screen.blit(img, (gx, pac_y))
                    ghosts_visible+=1
            if ghosts_visible==0 and pac_x<-100:
                state="menu"

        elif state=="menu":
            hover=get_hover()
            screen.blit(menu_bgs[hover], (0, 0))
            
            #random ghosts crossing the menu
            if not crossing:
                if time.time()-last_exit>spawn_delay:
                    crossing=True
                    g_img=random.choice(ghost_imgs)
                    lane=random.randint(1, 4)
                    reverse=random.randint(0, 1)
                    
                    #pick a lane
                    if lane==1 or lane==2:
                        g_dir="horizontal"
                        if reverse==1:
                            gx=WIDTH+150
                            g_speed=-5
                            p_draw=pac_img
                            g_draw=g_img
                        else:
                            gx=-150
                            g_speed=5
                            p_draw=pygame.transform.flip(pac_img, True, False)
                            g_draw=pygame.transform.flip(g_img, True, False)
                        gy=670 if reverse==1 else 210
                    if lane==3 or lane==4:
                        g_dir="vertical"
                        if reverse==1:
                            gy=HEIGHT+150
                            g_speed=-5
                            p_draw=pygame.transform.rotate(pac_img, -90)
                            g_draw=pygame.transform.rotate(g_img, 90)
                            g_draw=pygame.transform.flip(g_draw, False, True)
                        else:
                            gy=-50
                            g_speed=5
                            p_draw=pygame.transform.rotate(pac_img, 90)
                            g_draw=pygame.transform.rotate(g_img, -90)
                            g_draw=pygame.transform.flip(g_draw, True, True)
                        gx=60 if lane==3 else 820
                    
            else:
                if g_dir=="horizontal":
                    gx+=g_speed
                    if g_speed>0:
                        ghost_x=gx-100
                    else:
                        ghost_x=gx+100
                    ghost_y=gy
                else:
                    gy+=g_speed
                    if g_speed>0:
                        ghost_y=gy-100
                    else: 
                        ghost_y=gy+100
                    ghost_x=gx

                screen.blit(p_draw, (gx, gy))
                screen.blit(g_draw, (ghost_x, ghost_y))

                #check if they left
                if g_dir=="horizontal":
                    if gx>WIDTH+200 or gx<-200:
                        crossing=False
                        last_exit=time.time()
                else:
                    if gy>HEIGHT+200 or gy<-200:
                        crossing=False
                        last_exit=time.time()

        
            draw_players()

            title_txt = font_big.render("CHOOSE YOUR GAME", True, WHITE)
            screen.blit(title_txt, title_txt.get_rect(center=(WIDTH//2, 165)))

            
            if hover<=5:
                name_txt=font_small.render(games_list[hover], True, WHITE)
                screen.blit(name_txt, name_txt.get_rect(center=(WIDTH//2, 235)))

            #back button
            back_hover=back_rect.collidepoint(mouse_pos)
            back_color=YELLOW if back_hover else WHITE
            back_txt=font_small.render("BACK", True, back_color)
            screen.blit(back_txt, (WIDTH-120, HEIGHT-50))

        pygame.display.flip()
        FPS.tick(60)

    pygame.quit()
