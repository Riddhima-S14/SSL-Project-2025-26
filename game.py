import pygame 
from pygame.locals import *
import numpy as np
pygame.init()
class games:
    def __init__(self, player1, player2, board = np.zeros(5)):
        self.active = 1
        self.n_active = 2
        self.board = board
        self.winner = None
    def switch(self):
        self.active, self.n_active = self.n_active, self.active
    def win_check(self):
        pass
    def display(self):
        print(self.board)
    def is_board_full(self):
        return not np.any(self.board==0)
