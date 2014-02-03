from game_state import *

import label
import minimax


class Player(object):
    def __init__(self, color):
        self.color = color

    def make_move(self, state):
        state.draw_board()


class BotPlayer(object):
    def __init__(self, color):
        self.color = color
        self.solver = minimax.Minimax(self.color)

    def make_move(self, state):
        move, score = self.solver.minimax(state)
        return move


class HumanPlayer(object):
    def __init__(self, color):
        self.color = color

    def make_move(self, state):
        state.draw_board()
        print('Make a move, sir')

        pawn = None
        valid = False
        print('Begin by selecting a pawn in a row and column')
        while not valid:
            row, col = eval(input('row, col: '))
            pawn = state.get_pawn(row, col, self.color)
            if pawn is not None:
                valid = True
        final_pos = None
        valid = False
        print('Select a final position for the pawn')
        while not valid:
            row, col = eval(input('row, col: '))
            if state.check_cell(row, col) == label.BLANK:
                final_pos = Position(row, col)
                valid = True

        return Move(pawn, final_pos)
