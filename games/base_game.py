import numpy as np

class games:
    def __init__(self, player1, player2, board=np.zeros(5)):
        self.player1 = player1
        self.player2 = player2
        self.active = player1
        self.n_active = player2
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
