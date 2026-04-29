import sys
import time
import datetime
import pygame
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#backend that renders images directly to files (PNG) instead of opening a GUI window
matplotlib.use('Agg')


class games_class:
    def _init_(self, player1, player2, board=np.zeros(5)):
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

#input names from the command line

if len(sys.argv)>1:
    player1=sys.argv[1]
    player2=sys.argv[2]
else:
    player1="s"
    player2="r"

#setting up paths
BASE_PATH=os.path.dirname(_file_)
ASSETS_DIR=os.path.join(BASE_PATH, 'assets')


#fonts
font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
font_big=pygame.font.Font(font_path, 32)
font_medium=pygame.font.Font(font_path, 26)
font_small=pygame.font.Font(font_path, 18)
font_name=pygame.font.Font(font_path, 14)

#load backgrounds
bg_main=pygame.image.load(os.path.join(ASSETS_DIR, "bg_main.png")).convert()
bg_stats=pygame.image.load(os.path.join(ASSETS_DIR, "stats.png")).convert()

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

post_bgs=[]
post_names=["post.png", "post1.png", "post2.png", "post3.png", "post4.png"]

leaderboard_bgs=[]
leaderboard_names=["leaderboard.png", "l_1.png", "l_2.png", "l_3.png", "l_4.png", "l_5.png", "l_6.png"]

icons=[]
icon_names=["ttt.png", "c4.png", "o.png", "bs.png", "p.png"]

def load_images(a, b):
    for name in a:
        path=os.path.join(ASSETS_DIR, name)
        b.append(pygame.image.load(path).convert())

load_images(menu_names, menu_bgs)
load_images(post_names, post_bgs)
load_images(leaderboard_names, leaderboard_bgs)
load_images(icon_names, icons)

    
games_list=["", "TIC-TAC-TOE", "CONNECT-4", "OTHELLO", "BATTLESHIP", "PONG"]

#option boxes (menu)
box_rects = [
    pygame.Rect(130, 280, 165, 170),
    pygame.Rect(365, 280, 165, 170),
    pygame.Rect(600, 280, 165, 170),
    pygame.Rect(252, 480, 165, 170),
    pygame.Rect(490, 480, 165, 170)
]

#position boxes (post game)
post_rects = [
    pygame.Rect(180, 100, 540, 130),
    pygame.Rect(180, 265, 540, 130),
    pygame.Rect(180, 430, 540, 130),
    pygame.Rect(180, 600, 540, 130)
]

#position boxes (leaderboard page)
leaderboard_rects = [
    pygame.Rect(332, 130, 260, 60),
    pygame.Rect(332, 217, 260, 60),
    pygame.Rect(332, 307, 260, 60),
    pygame.Rect(332, 485, 260, 60),
    pygame.Rect(332, 575, 260, 60),
    pygame.Rect(332, 663, 260, 60),
]

#position boxes(icons)
icon_rects =[
    pygame.Rect(150, 290, 140, 140), 
    pygame.Rect(387, 290, 140, 140), 
    pygame.Rect(621, 290, 140, 140), 
    pygame.Rect(276, 490, 140, 140), 
    pygame.Rect(512, 490, 140, 140)
]


#rectangles for buttons
back_rect=pygame.Rect(750, 680, 100, 40)
stats_exit_rect=pygame.Rect(WIDTH - 150, 20, 130, 40)
stats_leaderboard_rect=pygame.Rect(20, HEIGHT - 60, 280, 40)
stats_play_again_rect=pygame.Rect(WIDTH-200, HEIGHT - 60, 180, 40)

#menu animation variables
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
current_game=""
show_terminal_msg=False
terminal_msg_time=0


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
def get_hover_menu():
    mouse_pos=pygame.mouse.get_pos()
    for i, rect in enumerate(box_rects):
        if rect.collidepoint(mouse_pos):
            return i + 1
    return 0

#for the post game menu
def get_hover_post():
    mouse_pos=pygame.mouse.get_pos()
    for i, rect in enumerate(post_rects):
        if rect.collidepoint(mouse_pos):
            return i + 1
    return 0

#for the leaderboard menu
def get_hover_leaderboard():
    mouse_pos=pygame.mouse.get_pos()
    for i, rect in enumerate(leaderboard_rects):
        if rect.collidepoint(mouse_pos):
            return i + 1
    return 0

winner=0

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

#write into history.csv  
def history(w,l,game):
    with open(os.path.join(BASE_PATH, "history.csv"), 'a', newline="\n") as f:
        f.write(w+','+l+','+game+','+datetime.datetime.today()+'\n')

#update history
def update(winner,game):
    if not( winner == 0.5 or winner == 0):
        loser = player1 if (winner == player2) else player2
        history(winner,loser,game)

#function for updating dictionnary for existing and non existing keys
def dict_update(value,d):
    if value not in d.keys():
        d[value] = 1
    else:
        d[value] += 1 
#drawing the plots
def plots(file_name):
    win_dict = dict()
    lose_dict = dict()
    game_dict = dict()

    #avoid crashing on the first run
    if not os.path.exists(file_name):
        return

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line_raw in lines:
            #deal with carriage return issues
            line_str = line_raw.strip()
            if not line_str:
                continue

            line = line_str.split(',')
#safe check for if history.csv has invalid lines
            if len(line) < 3:
                continue

            winner = line[0].strip()
            loser = line[1].strip()
            game = line[2].strip()

            if not winner or not loser or not game:
                continue
#update the winners, losers and game dictionnary
            dict_update(winner, win_dict)
            dict_update(loser, lose_dict)
            dict_update(game, game_dict)
#for players with 0 wins or 0 losses
            if line[1] not in win_dict:
                win_dict[line[1]] = 0
            if line[0] not in lose_dict:
                lose_dict[line[0]] = 0
#sorting dictionnary for top 5
    sorted_win = dict(sorted(win_dict.items(), key=lambda item: item[1], reverse=True))
    
    top5 = list()
    top5_scores = list()
    
    for i in range(0, min(5, len(list(sorted_win.keys())))):
        player_name = list(sorted_win.keys())[i]
        top5.append(player_name)
        top5_scores.append(win_dict[player_name])
#creating the figures with high resolution
    fig1 = plt.figure(figsize=(6, 5), dpi=300)
    plt.bar(top5, top5_scores, color='teal', edgecolor='black')
    plt.title('Top 5 Players', fontsize=14)
    plt.xlabel('Players')
    plt.ylabel('Wins')
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_PATH, "Top_5.png"))
    plt.close(fig1)

    if game_dict:
        plays = list(game_dict.values())
        labels = list(game_dict.keys())

        fig2 = plt.figure(figsize=(6, 5), dpi=300)
        plt.pie(plays, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Most Played Games", fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(BASE_PATH, "Games.png"))
        plt.close(fig2)
            

running=True
if _name_ == "_main_":
    history_path = os.path.join(BASE_PATH, "history.csv")
    if os.path.exists(history_path):
        plots(history_path)
    while running:
        mouse_pos=pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            #press enter to start
            if event.type==pygame.KEYDOWN:
                if state=="main" and event.key==pygame.K_RETURN:
                    state="animation"
                    pac_x=WIDTH #reset the animation
        
            #if there's a click
            if event.type==pygame.MOUSEBUTTONDOWN:

                if state=="post_game":
                    hover=get_hover_post()
                    #which button
                    if hover==1:
                        state="leaderboard"
                    elif hover==2:
                        state="stats"
                    elif hover==3:
                        state="menu"
                    elif hover==4:
                        running=False
                        pygame.quit()

                elif state=="menu":
                    hover=get_hover_menu()
                    #which button
                    if hover!=0:
                        winner=launch_game(hover)
                        current_game=games_list[hover]
                        #update history.csv
                        update(winner,games_list[hover])
                        plots(os.path.join(BASE_PATH, "history.csv"))
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Game Hub")
                        if winner==0:
                            state="menu"
                        else:
                            state="post_game"
                        #print(state)
                    elif back_rect.collidepoint(mouse_pos):
                        state="main"

                elif state=="leaderboard":
                    hover=get_hover_leaderboard()
                    #which button
                    sort_type = 0
                    if hover == 1: sort_type=1
                    elif hover == 2: sort_type=2
                    elif hover == 3: sort_type=3
                    
                    if hover in [1, 2, 3]:
                        os.system('clear')
                        os.system(f"bash leaderboard.sh {current_game} {sort_type}")
                        show_terminal_msg = True
                        terminal_msg_time = time.time()

                    elif hover==4:
                        state="stats"
                    elif hover==5:
                        state="menu"
                    elif hover==6:
                        pygame.quit()

                elif state == "stats":
                    if stats_exit_rect.collidepoint(mouse_pos):
                        running=False
                        pygame.quit()
                        sys.exit()
                    elif stats_leaderboard_rect.collidepoint(mouse_pos):
                        state="leaderboard"
                    elif stats_play_again_rect.collidepoint(mouse_pos):
                        state="menu"
                    
                '''if state=="post_game":
                    hover=get_hover_post()
                    if hover==1:
                        state="leaderboard"
                    elif hover==2:
                        state="stats"
                    elif hover==3:
                        state="menu"
                    elif hover==4:
                        running=False
                        pygame.quit()'''
                
                

        #for blinking animation
        if time.time()-last_blink>0.5:
            show_blink=not show_blink
            last_blink=time.time()

        #print(state)

        if state=="main":
            screen.blit(bg_main, (0, 0))
            draw_players()
            #show "insert coin"
            if show_blink:
                blink_txt=font_medium.render("INSERT COIN TO START", True, YELLOW)
                screen.blit(blink_txt, blink_txt.get_rect(center=(WIDTH//2, 395)))

        elif state=="animation":
            screen.blit(bg_main, (0, 0))
            draw_players()
            pac_x-=speed
            screen.blit(pac_img, (pac_x, pac_y))
            ghosts_visible=0
            #animate the ghosts moving across the screen
            for i, img in enumerate(ghost_imgs):
                gx=pac_x+initial_gap+(i*ghost_gap)
                if gx+img.get_width()>0:
                    screen.blit(img, (gx, pac_y))
                    ghosts_visible+=1
            #next screen when it's done
            if ghosts_visible==0 and pac_x<-100:
                state="menu"

        elif state=="menu":
            hover=get_hover_menu()
            #background images based on hover
            screen.blit(menu_bgs[hover], (0, 0))
            for i, rect in enumerate(icon_rects):
                if i < len(icons):
                    img = pygame.transform.scale(icons[i], (rect.width, rect.height))
                    screen.blit(img, rect.topleft)
            
            #random ghosts crossing the menu
            if not crossing:
                if time.time()-last_exit>spawn_delay:
                    crossing=True
                    g_img=np.random.choice(ghost_imgs)
                    lane=np.random.randint(1, 5)
                    reverse=np.random.randint(0, 2)
                    
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

            #game name display
            if hover<=5:
                name_txt=font_small.render(games_list[hover], True, WHITE)
                screen.blit(name_txt, name_txt.get_rect(center=(WIDTH//2, 235)))

            #back button
            back_hover=back_rect.collidepoint(mouse_pos)
            back_color=YELLOW if back_hover else WHITE
            back_txt=font_small.render("BACK", True, back_color)
            screen.blit(back_txt, (WIDTH-120, HEIGHT-50))

        elif state=="post_game":
            screen.blit(post_bgs[0], (0, 0))

            """txt = font_medium.render("POST GAME SCREEN", True, YELLOW)
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 120)))

            draw_players()"""

            hover=get_hover_post()
            screen.blit(post_bgs[hover], (0, 0))

            draw_players()
        
        elif state=="leaderboard":
            hover=get_hover_leaderboard()
            screen.blit(leaderboard_bgs[hover], (0, 0))

    
            if show_terminal_msg:
                elapsed = time.time() - terminal_msg_time
                if elapsed < 3.0: 
                    term_txt = font_name.render("DISPLAYED ON TERMINAL", True, WHITE)
                    text_rect = term_txt.get_rect(center=(WIDTH//2 + 20, 420))
                    screen.blit(term_txt, text_rect)
                else:
                    show_terminal_msg = False

        elif state=="stats":

            screen.blit(bg_stats, (0, 0))

            top5_path = os.path.join(BASE_PATH, "Top_5.png")
            games_path = os.path.join(BASE_PATH, "Games.png")

            if os.path.exists(top5_path) and os.path.exists(games_path):
                top5_img = pygame.image.load(top5_path)
                games_img = pygame.image.load(games_path)
        
                top5_img = pygame.transform.scale(top5_img, (400, 330))
                games_img = pygame.transform.scale(games_img, (400, 330))
        
                screen.blit(top5_img, (40, 150))
                screen.blit(games_img, (460, 150))
            else:
                msg = font_small.render("NO STATS AVAILABLE YET", True, WHITE)
                screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            
            #buttons
            exit_h = stats_exit_rect.collidepoint(mouse_pos)
            exit_color = YELLOW if exit_h else WHITE
            exit_txt = font_small.render("EXIT", True, exit_color)
            screen.blit(exit_txt, (WIDTH - 140, 30))

            lead_h = stats_leaderboard_rect.collidepoint(mouse_pos)
            lead_color = YELLOW if lead_h else WHITE
            lead_txt = font_small.render("LEADERBOARD", True, lead_color)
            screen.blit(lead_txt, (30, HEIGHT - 50))

            play_h = stats_play_again_rect.collidepoint(mouse_pos)
            play_color = YELLOW if play_h else WHITE
            play_txt = font_small.render("PLAY AGAIN", True, play_color)
            screen.blit(play_txt, (WIDTH - 200, HEIGHT - 50))

        pygame.display.flip()

        FPS.tick(60)

    pygame.quit()
