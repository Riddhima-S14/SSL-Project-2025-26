import pygame 
from pygame.locals import *
import numpy as np
pygame.init()
class games:
    def __init__(self,active = 1,n_active = 2, board = np.zeros(5)):
        self.active = active
        self.n_active = n_active
        self.board = board
    def switch(self):
        x = self.active
        self.active = self.n_active
        self.n_active = x
    def win_check(self):
        pass
    def display(self):
        print(self.board)
