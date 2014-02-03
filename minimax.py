from copy import deepcopy


class Minimax(object):
    def __init__(self, color):
        self.color = color

    def minimax(self, state):
        """Initiates a minimax search on the current game state."""
        return max(
            map(lambda move: (move, -self.mmax(self.next_state(state, move))),
                state.get_available_moves()),
            key=lambda x: x[1])

    def mmax(self, state):
        """
        Maximizes the score against all of the next positions available
        for a specified game state.
        """
        if state.check_gameover():
            return self.evaluate(state)
        return max(
            map(lambda move: -self.mmax(self.next_state(state, move)),
                state.get_available_moves()))

    def evaluate(self, state):
        """Evaluates the state of a position for the configured player."""
        return float('inf') if state.winner == self.color else float('-inf')

    def next_state(self, state, move):
        """Returns the next state of the game given a current state and a move.

        Keyword arguments:
        state -- the current state of the game
        move -- the move to apply

        """
        clone = deepcopy(state)
        clone.make_move(move)
        clone.alternate_turn()
        return clone
