import label
import itertools


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
      print()
      print(' ', end=' ')
      blabels = [str(i) for i in range(3)]
      for ele in blabels:
        print("|",ele, end=" ")
      print('|')
      print('-'*15)
      i = 0
      for row in self.board:
        print(blabels[i], end = " ")
        i += 1
        for ele in row:
          print ("|",ele, end=" ")
        print("|")
        print('-'*15)
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

