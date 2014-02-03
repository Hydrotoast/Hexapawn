import random


class GameoverException(Exception):
    def __init__(self, move):
        self.move = move


class Oracle(object):
    def __init__(self):
        self.__last_state = None
        self.__last_move = None

        self.learned = dict()

    def consult(self, state):
        # Add state to dictionary if it does not exist
        if state not in self.learned:
            self.learned[repr(state)] = state.get_available_moves()

        # If the state has no moves, it is a gameover
        if len(self.learned[repr(state)]) == 0:
            self.loss(self.last_state, self.last_move)
            raise GameoverException("Gameover.")
            return

        self.last_state = state
        self.last_move = self.learned[repr(state)][random.randint(0, len(self.learned[repr(state)])-1)]
        return self.last_move

    def loss(self, state, move):
        if move in self.learned[state]:
            self.learned[repr(state)].remove(move)

    @property
    def last_state(self):
        return self.__last_state

    @last_state.setter
    def last_state(self, state):
        self.__last_state = state

    @property
    def last_move(self):
        return self.__last_move

    @last_move.setter
    def last_move(self, move):
        self.__last_move = move
