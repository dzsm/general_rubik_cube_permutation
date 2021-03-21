# Copyright 2021 David Zsolt Manrique
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.

# https://en.wikipedia.org/wiki/Rubik%27s_family_cubes_of_all_sizes

import numpy


class RubikCubePermutation(object):
    _FACE = {'U': 0, 'D': 1, 'F': 2, 'B': 3, 'R': 4, 'L': 5}
    _INVERSE_FACE = ['U', 'D', 'F', 'B', 'R', 'L']

    def __init__(self, n: int):

        # CUBE of n x n x n
        self._n = n
        self._n2 = self._n ** 2

        # TWO KINDS OF STATE : FACE STATE AND FLATTENED STATE
        self._idx = numpy.array(range(6 * self._n ** 2), dtype=int)
        self._idx_6nn = self._idx.copy().reshape((6, self._n, self._n))
        self._face_idx = self._idx // self._n ** 2
        self._face_idx_6nn = self._face_idx.copy().reshape((6, self._n, self._n))

        # INDEX WIDTH FOR PRINTING
        self._field_width = int(numpy.round(numpy.log10(max(self._idx)) + 1))

        # GRID FOR PRINTING
        unfolded_grid = numpy.full((3 * self._n, 4 * self._n), -1, dtype=int)

        for r in range(self._n):
            for c in range(self._n):
                unfolded_grid[r, c + self._n] = self._idx_6nn[0, r, c]
                unfolded_grid[r + self._n, c + self._n] = self._idx_6nn[2, r, c]
                unfolded_grid[r + 2 * self._n, c + self._n] = self._idx_6nn[1, r, c]
                unfolded_grid[r + self._n, c] = self._idx_6nn[5, r, c]
                unfolded_grid[r + self._n, c + 2 * self._n] = self._idx_6nn[4, r, c]
                unfolded_grid[r + self._n, c + 3 * self._n] = self._idx_6nn[3, r, c]

        self._unfolded_grid = unfolded_grid

        unfolded = []
        for r in range(unfolded_grid.shape[0]):
            for c in range(unfolded_grid.shape[1]):
                if unfolded_grid[r, c] >= 0:
                    unfolded.append(unfolded_grid[r, c])

        self._unfolded = numpy.asarray(unfolded)

        # OPERATIONS

        uw_move = lambda layer: uw_move(layer - 1)[self.perm_u(layer)] if layer > 0 else self.perm_u(layer)
        fw_move = lambda layer: fw_move(layer - 1)[self.perm_f(layer)] if layer > 0 else self.perm_f(layer)
        rw_move = lambda layer: rw_move(layer - 1)[self.perm_r(layer)] if layer > 0 else self.perm_r(layer)

        inner_layer_moves = []
        outer_layer_moves = []
        for m in range((self._n + 1) // 2):
            u = self.perm_u(m)
            f = self.perm_f(m)
            r = self.perm_r(m)
            for p, l in [(u, 'U'), (f, 'F'), (r, 'R')]:
                if m == 0:
                    outer_layer_moves.append((f'{l}', p))
                    outer_layer_moves.append((f'{l}2', p[p]))
                    outer_layer_moves.append((f'{l}\'', p[p[p]]))
                else:
                    inner_layer_moves.append((f'{m + 1}{l}', p))
                    inner_layer_moves.append((f'{m + 1}{l}2', p[p]))
                    inner_layer_moves.append((f'{m + 1}{l}\'', p[p[p]]))

            for p, l in [(u[u[u]], 'D'), (f[f[f]], 'B'), (r[r[r]], 'L')]:
                if m == self._n - 1:
                    outer_layer_moves.append((f'{l}', p))
                    outer_layer_moves.append((f'{l}2', p[p]))
                    outer_layer_moves.append((f'{l}\'', p[p[p]]))
                else:
                    inner_layer_moves.append((f'{self._n - m}{l}', p))
                    inner_layer_moves.append((f'{self._n - m}{l}2', p[p]))
                    inner_layer_moves.append((f'{self._n - m}{l}\'', p[p[p]]))

        outer_block_moves = []
        for m in range((self._n + 1) // 2):
            uw = uw_move(m)
            fw = fw_move(m)
            rw = rw_move(m)
            for p, l in [(uw, 'Uw'), (fw, 'Fw'), (rw, 'Rw')]:
                if m != 0:
                    outer_block_moves.append((f'{m + 1}{l}', p))
                    outer_block_moves.append((f'{m + 1}{l}2', p[p]))
                    outer_block_moves.append((f'{m + 1}{l}\'', p[p[p]]))

            for p, l in [(uw[uw[uw]], 'Dw'), (fw[fw[fw]], 'Bw'), (rw[rw[rw]], 'Lw')]:
                if m != self._n - 1:
                    outer_block_moves.append((f'{self._n - m}{l}', p))
                    outer_block_moves.append((f'{self._n - m}{l}2', p[p]))
                    outer_block_moves.append((f'{self._n - m}{l}\'', p[p[p]]))

        y = uw_move(self._n - 1)
        z = fw_move(self._n - 1)
        x = rw_move(self._n - 1)

        rotations = []
        for p, l in [(x, 'X'), (y, 'Y'), (z, 'Z')]:
            rotations.append((f'{l}', p))
            rotations.append((f'{l}2', p[p]))
            rotations.append((f'{l}\'', p[p[p]]))

        self._rotations = {k: v for k, v in rotations}
        self._outer_layer_moves = {k: v for k, v in outer_layer_moves}
        self._inner_layer_moves = {k: v for k, v in inner_layer_moves}
        self._outer_block_moves = {k: v for k, v in outer_block_moves}

        self._moves = dict(**self._rotations, **self._outer_layer_moves, **self._inner_layer_moves,
                           **self._outer_block_moves)

        self._ldb_l = self._idx_6nn[5, self._n - 1, 0]
        self._ldb_d = self._idx_6nn[1, self._n - 1, 0]
        self._ldb_b = self._idx_6nn[3, self._n - 1, self._n - 1]

    def perm_id(self):
        return self._idx.copy()

    def perm_u(self, layer):

        idx_6nn = self._idx_6nn.copy()

        if layer == 0:
            idx_6nn[0] = numpy.rot90(idx_6nn[0], 3)
        elif layer == self._n - 1:
            idx_6nn[1] = numpy.rot90(idx_6nn[1], 1)

        t = idx_6nn[2, layer, :].copy()
        idx_6nn[2, layer, :] = idx_6nn[4, layer, :]
        idx_6nn[4, layer, :] = idx_6nn[3, layer, :]
        idx_6nn[3, layer, :] = idx_6nn[5, layer, :]
        idx_6nn[5, layer, :] = t

        return idx_6nn.flatten()

    def perm_f(self, layer):

        idx_6nn = self._idx_6nn.copy()

        if layer == 0:
            idx_6nn[2] = numpy.rot90(idx_6nn[2], 3)
        elif layer == self._n - 1:
            idx_6nn[3] = numpy.rot90(idx_6nn[3], 1)

        reverse_layer = self._n - 1 - layer

        t = idx_6nn[0, reverse_layer, :].copy()
        idx_6nn[0, reverse_layer, :] = idx_6nn[5, ::-1, reverse_layer]
        idx_6nn[5, :, reverse_layer] = idx_6nn[1, layer, :]
        idx_6nn[1, layer, :] = idx_6nn[4, ::-1, layer]
        idx_6nn[4, :, layer] = t

        return idx_6nn.flatten()

    def perm_r(self, layer):

        idx_6nn = self._idx_6nn.copy()

        if layer == 0:
            idx_6nn[4] = numpy.rot90(idx_6nn[4], 3)
        elif layer == self._n - 1:
            idx_6nn[5] = numpy.rot90(idx_6nn[5], 1)

        reverse_layer = self._n - 1 - layer

        t = idx_6nn[0, :, reverse_layer].copy()
        idx_6nn[0, :, reverse_layer] = idx_6nn[2, :, reverse_layer]
        idx_6nn[2, :, reverse_layer] = idx_6nn[1, :, reverse_layer]
        idx_6nn[1, :, reverse_layer] = idx_6nn[3, ::-1, layer]
        idx_6nn[3, ::-1, layer] = t

        return idx_6nn.flatten()

    def perm_moves(self, moves: str):
        move_list = [move.strip() for move in moves.strip().split()]

        p = self._moves[move_list[0]]
        for i in range(1, len(move_list)):
            p = p[self._moves[move_list[i]]]

        return p

    def print_definition(self):

        print('# State indices, face indices, orientation [U]P [D]OWN [F]RONT [B]ACK [L]EFT [R]IGHT:')
        for r in range(self._unfolded_grid.shape[0]):
            for c in range(self._unfolded_grid.shape[1]):
                if self._unfolded_grid[r, c] < 0:
                    print(f' {" ":{self._field_width}s} ', end='')
                else:
                    print(f' {self._unfolded_grid[r, c]:{self._field_width}d} ', end='')

            print(f'   {" ":{self._field_width}s}   ', end='')

            for c in range(self._unfolded_grid.shape[1]):
                if self._unfolded_grid[r, c] < 0:
                    print(f' {" ":{self._field_width}s} ', end='')
                else:
                    print(f' {self._face_idx[self._unfolded_grid[r, c]]:{self._field_width}d} ',
                          end='')

            print(f'   {" ":{self._field_width}s}   ', end='')

            for c in range(self._unfolded_grid.shape[1]):
                if self._unfolded_grid[r, c] < 0:
                    print(f' {" ":{self._field_width}s} ', end='')
                else:
                    print(
                        f' {self._INVERSE_FACE[self._face_idx[self._unfolded_grid[r, c]]]:>{self._field_width}s} ',
                        end='')

            print()
        print()

    def initial_state(self):
        return numpy.array(range(6 * self._n ** 2), dtype=int) // self._n ** 2

    def is_state_ldb_normalized(self, state):

        return state[self._ldb_l] == 5 and state[self._ldb_d] == 1 and state[self._ldb_b] == 3

    def is_state_solved(self, state):

        idx = 0
        for f in range(6):
            ref = state[idx]
            idx += 1
            for i in range(1, self._n2):
                if ref != state[idx]:
                    return False
                idx += 1

        return True


if __name__ == "__main__":
    print('# Cube 2x2x2:')
    c2 = RubikCubePermutation(2)
    c2.print_definition()

    p = c2.perm_moves('U2 F')
    print('# Permutation on state array: ')
    print(p)

    print()

    print('# Cube 2x2x2:')
    c4 = RubikCubePermutation(4)
    c4.print_definition()

    p = c4.perm_moves('U2 F')
    print('# Permutation on state array: ')
    print(p)
