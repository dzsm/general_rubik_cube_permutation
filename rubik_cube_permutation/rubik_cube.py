import numpy
from .rubik_cube_permutation import RubikCubePermutation


class RubikCube(RubikCubePermutation):
    _COLOR = {'W': 0, 'Y': 1, 'G': 2, 'B': 3, 'R': 4, 'O': 5} # Western coloring scheme
    _INVERSE_COLOR = ['W', 'Y', 'G', 'B', 'R', 'O']

    def __init__(self, n: int):
        super().__init__(n)

        self._state = self.initial_state()

    def get_scrambler_moves(self, n: int, seed: int):
        move_list = sorted(list(self._outer_layer_moves.keys()) + list(self._outer_block_moves.keys()))
        random = numpy.random.RandomState(seed)
        return ' '.join(random.choice(move_list, n))

    def reset(self):
        self._state = self.initial_state()
        return self

    def scramble(self, n: int, seed: int):
        self.move(self.get_scrambler_moves(n, seed))
        return self

    def move(self, moves: str):
        p = self.perm_moves(moves)
        self._state = self._state[p]
        return self

    def print_state(self):

        for r in range(self._unfolded_grid.shape[0]):
            for c in range(self._unfolded_grid.shape[1]):
                if self._unfolded_grid[r, c] < 0:
                    print(f' {" ":{self._field_width}s} ', end='')
                else:
                    print(f' {self._INVERSE_COLOR[self._state[self._unfolded_grid[r, c]]]:>{self._field_width}s} ',
                          end='')

            print()
        print()

        return self

    def print_move(self, moves: str, steps=False, move=False):

        move_steps = [moves]
        state = self._state.copy()

        if steps:
            move_steps = [op.strip() for op in moves.split()]

        for move in move_steps:

            p = self.perm_moves(move)
            next_state = state[p]

            print(move)
            for r in range(self._unfolded_grid.shape[0]):
                for c in range(self._unfolded_grid.shape[1]):
                    if self._unfolded_grid[r, c] < 0:
                        print(f' {" ":{self._field_width}s} ', end='')
                    else:
                        print(f' {self._INVERSE_COLOR[state[self._unfolded_grid[r, c]]]:>{self._field_width}s} ',
                              end='')

                # if r == self._unfolded_grid.shape[0] // 2:
                print(f'    ==>   ', end='')
                # else:
                #    print(f'   {" ":{self._field_width}s}   ', end='')

                for c in range(self._unfolded_grid.shape[1]):
                    if self._unfolded_grid[r, c] < 0:
                        print(f' {" ":{self._field_width}s} ', end='')
                    else:
                        print(f' {self._INVERSE_COLOR[next_state[self._unfolded_grid[r, c]]]:>{self._field_width}s} ',
                              end='')

                print()
            state = next_state
            print()

        if move:
            self._state = state

        return self

    def set_state_from_print(self, text: str):
        unfolded_state = [self._COLOR[color] for color in text.replace(' ', '').replace('\n', '')]

        for i, k in enumerate(self._unfolded):
            self._state[k] = unfolded_state[i]

        return self


if __name__ == "__main__":
    c = RubikCube(2)

    c.print_definition()

    text = '''
              W   W                         
              W   W                         
      R   R   B   B   O   O   G   G         
      Y   B   Y   Y   B   Y   G   G         
              O   R                         
              R   O                         
    '''

    c.print_state().move('U R').print_state()
    c.reset().print_move('U', True)
