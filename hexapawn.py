import label
import minimax
import oracle

import itertools
import os


class Position(object):
    """Defines a position on the board."""
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return '(%d, %d)' % (self.row, self.col)


class Piece(object):
    """Defines a position on the board."""
    def __init__(self, state, color, pos):
        self.state = state
        self.color = color
        self.pos = pos

    def get_moves(self):
        """ Returns a list of all possible moves from this piece."""
        row_offset = 1 if self.color == label.RED else -1
        left_offset = -1
        right_offset = 1

        moves = []

        # Try advance
        if self.state.check_cell(self.pos.row + row_offset, self.pos.col) == label.BLANK:
            moves.append(Move(self, Position(self.pos.row + row_offset, self.pos.col)))

        # Left attack
        if self.state.check_cell(self.pos.row + row_offset, self.pos.col + left_offset) == \
                label.get_opposite(self.color):
            moves.append(Move(self, Position(self.pos.row + row_offset, self.pos.col + left_offset)))

        # Right attack
        if self.state.check_cell(self.pos.row + row_offset, self.pos.col + right_offset) == \
                label.get_opposite(self.color):
            moves.append(Move(self, Position(self.pos.row + row_offset, self.pos.col + right_offset)))

        return moves

    @property
    def row(self):
        return self.pos.row

    @property
    def col(self):
        return self.pos.col

    def __repr__(self):
        return "%s at %s" % (self.color, self.pos)


class Move(object):
    def __init__(self, pawn, pos):
        self.pawn = pawn
        self.pos = pos

    def __repr__(self):
        return "%s %s" % (self.pawn, self.pos)


class Player(object):
    def __init__(self, color):
        self.color = color

    def make_move(self, state):
        state.draw_board()


class HexapawnState(object):
    """The game of Hexapawn."""
    def __init__(self, width):
        self.width = width

        self.board = []
        self.board.append([label.RED] * self.width)
        self.board.append([label.BLANK] * self.width)
        self.board.append([label.BLUE] * self.width)

        self.__turn = label.RED
        self.__gameover = False
        self.winner = None

    def get_available_moves(self):
        """Returns the set of available moves."""
        pawns = []

        # Scan the playable pawns on the board
        for i, j in itertools.product(range(3), range(self.width)):
            if self.board[i][j] == self.turn:
                pawns.append(Piece(self, self.turn, Position(i, j)))

        moves = []
        for pawn in pawns:
            for move in pawn.get_moves():
                moves.append(move)

        return moves

    def make_move(self, move):
        """Makes a move on the game board."""
        self.board[move.pawn.row][move.pawn.col] = label.BLANK
        self.board[move.pos.row][move.pos.col] = move.pawn.color

    def alternate_turn(self):
        """Alternates the player turn on the board."""
        self.turn = label.get_opposite(self.turn)

    def check_gameover(self):
        """Checks if the gameover state has occurred."""
        # Check no piece end
        red = 0
        blue = 0
        for i, j in itertools.product(range(3), range(self.width)):
            if self.board[i][j] == label.RED:
                red += 1
            elif self.board[i][j] == label.BLUE:
                blue += 1
        if red == 0:
            self.winner = label.BLUE
            return True
        elif blue == 0:
            self.winner = label.RED
            return True

        # Check RED end line
        for i in range(self.width):
            if self.board[2][i] == label.RED:
                self.winner = label.RED
                return True

        # Check BLUE end line
        for i in range(self.width):
            if self.board[0][i] == label.BLUE:
                self.winner = label.BLUE
                return True

        # No moves available
        if len(self.get_available_moves()) == 0:
            self.winner = label.get_opposite(self.turn)
            return True

    def get_pawn(self, row, col, color):
        if self.check_cell(row, col) == color:
            return Piece(self, self.turn, Position(row, col))
        else:
            return None

    def check_cell(self, row, col):
        return -1 if row < 0 or row > (self.width - 1) or col < 0 or col > (self.width - 1) else self.board[row][col]

    def draw_board(self):
        for i in range(3):
            print(self.board[i])
        print()

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, value):
        self.__turn = value

    @property
    def gameover(self):
        return self.__gameover

    @gameover.setter
    def gameover(self, value):
        self.__gameover = value

    def __cmp__(self, other):
        if self.board < other:
            return -1
        elif self.board > other:
            return 1
        return 0

    def __str__(self):
        return '\n'.join(x for x in map(lambda x: str(x), self.board))

    def __repr__(self):
        return '\n'.join(x for x in map(lambda x: str(x), self.board))


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
            row = int(input('Row: '))
            col = int(input('Col: '))
            pawn = state.get_pawn(row, col, self.color)
            if pawn is not None:
                valid = True
        final_pos = None
        valid = False
        print('Select a final position for the pawn')
        while not valid:
            row = int(input('Row: '))
            col = int(input('Col: '))
            if state.check_cell(row, col) == label.BLANK:
                final_pos = Position(row, col)
                valid = True

        return Move(pawn, final_pos)


def solve_game():
    print('Solving game by minimax')
    state = HexapawnState(3)

    solver = minimax.Minimax(label.RED)
    move, score = solver.minimax(state)

    if score == float('inf'):
        print('Winner is RED player')
    else:
        print('Winner is BLUE player')


def play_game():
    state = HexapawnState(3)
    print('Select a color [r]/b?')
    player_wants_red = input() == 'r'

    if player_wants_red:
        print('You are RED')
        red = HumanPlayer(label.RED)
        blue = BotPlayer(label.BLUE)
    else:
        print('You are BLUE')
        red = BotPlayer(label.RED)
        blue = HumanPlayer(label.BLUE)

    while not state.check_gameover():
        move = red.make_move(state)
        state.make_move(move)
        state.alternate_turn()

        if state.check_gameover():
            break

        move = blue.make_move(state)
        state.make_move(move)
        state.alternate_turn()

    if state.winner == label.RED:
        print('Winner is RED player')
    else:
        print('Winner is BLUE player')


def oracle_learn():
    state = HexapawnState(5)

    red = oracle.Oracle()
    blue = oracle.Oracle()

    for i in range(100):
        while not state.check_gameover():
            move = red.consult(state)
            try:
                state.make_move(move)
                state.alternate_turn()
            except oracle.GameoverException:
                state.winner = label.BLUE
                red.loss(state, move)
                break

            if state.check_gameover():
                break

            move = blue.consult(state)
            try:
                state.make_move(move)
                state.alternate_turn()
            except oracle.GameoverException:
                state.winner = label.RED
                blue.loss(state, move)
                break

        if state.winner == label.RED:
            print('Winner is RED player')
        else:
            print('Winner is BLUE player')

    for state, moves in red.learned.items():
        print(state, moves, os.linesep)

    for state, moves in blue.learned.items():
        print(state, moves, os.linesep)


if __name__ == '__main__':
    print('Starting a game of Hexapawn (3x3)')
    print('RED player moves first')
    print()

    # oracle_learn()
    print('Solve for winner? [y]/n:')
    should_solve = input() == 'y'
    print()

    if should_solve:
        solve_game()
    else:
        play_game()
