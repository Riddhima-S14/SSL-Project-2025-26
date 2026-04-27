from game import games_class
import numpy as np
import time
import pygame
import random
import os
from pygame.locals import *

pygame.init()

# colours
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
YELLOW = (255,255,0)


class Battleship(games_class):
    def __init__(self, player1, player2, board_size=(10, 7)):
        super().__init__(player1, player2, np.zeros(board_size))
        # Updated to 10 Rows, 7 Columns
        self.board_p1 = np.zeros(board_size)
        self.board_p2 = np.zeros(board_size)
        self.place_ships(self.board_p1)
        self.place_ships(self.board_p2)
        self.hits_p1 = np.zeros(board_size)
        self.hits_p2 = np.zeros(board_size)


        BASE_PATH = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(BASE_PATH, '../assets')
        self.bg_main = pygame.image.load(os.path.join(ASSETS_DIR, "battleship_bg.png")).convert()
        
        self.font_path=os.path.join(ASSETS_DIR, "PressStart2P-Regular.ttf")
        self.font_big=pygame.font.Font(self.font_path, 50)
        self.font_medium=pygame.font.Font(self.font_path, 26)
        self.font_small=pygame.font.Font(self.font_path, 18)
        self.font_name=pygame.font.Font(self.font_path, 14)

    def place_ships(self, board):
        # Ship sizes
        ships = [5, 4, 3, 3, 2]
        for ship in ships:
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])
                if orientation == "H":
                    # Columns are now 7
                    r = random.randint(0, 10 - 1)
                    c = random.randint(0, 7 - ship)
                    if np.all(board[r, c:c + ship] == 0):
                        board[r, c:c + ship] = 1
                        placed = True
                else:
                    # Rows are now 10
                    r = random.randint(0, 10 - ship)
                    c = random.randint(0, 7 - 1)
                    if np.all(board[r:r + ship, c] == 0):
                        board[r:r + ship, c] = 1
                        placed = True

    def box(self, posn):
        CELL_SIZE = 40
        ROWS, COLS = 10, 7
        LEFT_BOARD_X = 75+50
        RIGHT_BOARD_X = 75+50 + (CELL_SIZE * COLS) + 100 
        Y_OFFSET = 165

        # Check Left Board (Player 1)
        if LEFT_BOARD_X <= posn[0] <= LEFT_BOARD_X + (CELL_SIZE * COLS) and \
           Y_OFFSET <= posn[1] <= Y_OFFSET + (CELL_SIZE * ROWS):
            x = (posn[0] - LEFT_BOARD_X) // CELL_SIZE
            y = (posn[1] - Y_OFFSET) // CELL_SIZE
            return (y, x, 1)

        # Check Right Board (Player 2)
        elif RIGHT_BOARD_X <= posn[0] <= RIGHT_BOARD_X + (CELL_SIZE * COLS) and \
             Y_OFFSET <= posn[1] <= Y_OFFSET + (CELL_SIZE * ROWS):
            x = (posn[0] - RIGHT_BOARD_X) // CELL_SIZE
            y = (posn[1] - Y_OFFSET) // CELL_SIZE
            return (y, x, 2)

        return (-1, -1, -1)

    def fire(self, target):
        y, x = target
        if self.active == 1:
            if self.hits_p2[y, x] == 0:
                self.hits_p2[y, x] = 1
                return True
        else:
            if self.hits_p1[y, x] == 0:
                self.hits_p1[y, x] = 1
                return True
        return False

    def win_check(self):
        if np.all((self.hits_p2 == 1) | (self.board_p2 == 0)):
            return self.player1
        elif np.all((self.hits_p1 == 1) | (self.board_p1 == 0)):
            return self.player2
        return 0

    def show(self, screen, mouse_pos):
              
       
        screen.blit(self.bg_main, (0, 0))
    

        # Labels
        p1_label=self.font_name.render("PLAYER 1", True, BLUE)
        p1_val=self.font_name.render(f"{self.player1}", True, BLUE)
        p2_label=self.font_name.render("PLAYER 2", True, GREEN)
        p2_val=self.font_name.render(f"{self.player2}", True, GREEN)
        screen.blit(p1_label, (50, 35))
        screen.blit(p1_val, (50, 60))
        screen.blit(p2_label, (900-180, 35))
        screen.blit(p2_val, (900-180, 60))

        # UI Buttons
        back_rect = pygame.Rect(750, 680, 100, 40)
        reset_rect = pygame.Rect(75, 680, 110, 40)

        back_color = YELLOW if back_rect.collidepoint(mouse_pos) else WHITE
        reset_color = YELLOW if reset_rect.collidepoint(mouse_pos) else WHITE
        
        screen.blit(self.font_small.render("BACK", True, back_color), (750, 685))
        screen.blit(self.font_small.render("RESET", True, reset_color), (75, 685))

    def execution(self):
        CELL_SIZE = 40
        ROWS, COLS = 10, 7
        LEFT_X = 75+50
        RIGHT_X = 455+50 # LEFT_X + (40 * 7) + 100 gap
        Y_OFFSET = 165
        CENTER = CELL_SIZE // 2

        display = pygame.display.set_mode((900, 750))
        pygame.display.set_caption("Battleship ")
        game_on = True
        end_time = None

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); exit()

                elif game_on and event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(750, 680, 100, 40).collidepoint(mouse_pos): 
                        return 0
                    if pygame.Rect(75, 680, 110, 40).collidepoint(mouse_pos):
                        self.board_p1=np.zeros((ROWS, COLS))
                        self.board_p2=np.zeros((ROWS, COLS))
                        self.hits_p1 = np.zeros((ROWS, COLS))
                        self.hits_p2 = np.zeros((ROWS, COLS))
                        self.place_ships(self.board_p1)
                        self.place_ships(self.board_p2)
                        self.active = 1
                        self.n_active = 2
                        self.winner = 0 
                        end_time = None
                        continue # Skip firing logic for this click
                    
                    y, x, target = self.box(event.pos)
                    if target != -1:
                        if (self.active == 1 and target == 2) or (self.active == 2 and target == 1):
                            if self.fire((y, x)):
                                if not ((target == 2 and self.board_p2[y,x] == 1) or (target == 1 and self.board_p1[y,x] == 1)):
                                    self.switch()
                                
                                winner = self.win_check()
                                if winner:
                                    self.winner = winner
                                    end_time = time.time()
                                    game_on = False
                
                


            self.show(display, mouse_pos)

            # Draw 10x7 Grids
            for i in range(ROWS + 1):
                py = Y_OFFSET + CELL_SIZE * i
                pygame.draw.line(display, WHITE if self.active ==1 else GREEN, (LEFT_X, py), (LEFT_X + CELL_SIZE * COLS, py), 2)
                pygame.draw.line(display, WHITE if self.active ==2 else BLUE, (RIGHT_X, py), (RIGHT_X + CELL_SIZE * COLS, py), 2)
            for i in range(COLS + 1):
                px_l = LEFT_X + CELL_SIZE * i
                px_r = RIGHT_X + CELL_SIZE * i
                pygame.draw.line(display, WHITE if self.active ==1 else GREEN, (px_l, Y_OFFSET), (px_l, Y_OFFSET + CELL_SIZE * ROWS), 2)
                pygame.draw.line(display, WHITE if self.active ==2 else BLUE, (px_r, Y_OFFSET), (px_r, Y_OFFSET + CELL_SIZE * ROWS), 2)
            pygame.draw.line(display,WHITE,(RIGHT_X-50,Y_OFFSET-25),(RIGHT_X-50,Y_OFFSET+10*CELL_SIZE+50))
            # Draw Hits/Misses
            for y in range(ROWS):
                for x in range(COLS):
                    if self.hits_p2[y, x] == 1:
                        color = GREEN if self.board_p2[y, x] == 1 else WHITE
                        pygame.draw.circle(display, color, (RIGHT_X + CENTER + x*CELL_SIZE, Y_OFFSET + CENTER + y*CELL_SIZE), 17)
                    
                    if self.hits_p1[y, x] == 1:
                        color = BLUE if self.board_p1[y, x] == 1 else WHITE
                        pygame.draw.circle(display, color, (LEFT_X + CENTER + x*CELL_SIZE, Y_OFFSET + CENTER + y*CELL_SIZE), 17)

            if not game_on and time.time()-end_time>0.75:
                font = pygame.font.SysFont(None, 72)
                if self.winner != 0:
                    text = self.font_medium.render(f"{self.winner} Wins!", True, WHITE)
                else:
                    text = self.font_medium.render("It's a Draw!", True, WHITE)
                rect = text.get_rect(center=(450, 375))
                pygame.draw.rect(display, BLACK, rect.inflate(40, 40))
                pygame.draw.rect(display, WHITE, rect.inflate(40, 40), 5)
                display.blit(text, rect)
                if not game_on and time.time()-end_time>2.5:
                        return self.winner 

            pygame.display.update()