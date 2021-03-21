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


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy

from .rubik_cube import RubikCube


class MplRubikCube(RubikCube):
    _RGB = ["#ffffff", "#ffd500", "#009b48", "#0046ad", "#b71234", "#ff5800"]
    _COLOR = {'W': 0, 'Y': 1, 'G': 2, 'B': 3, 'R': 4, 'O': 5}  # Western coloring scheme

    _EDGE_COLOR = '#111111'

    def __init__(self, n: int):
        super().__init__(n)

        self._fontsize = 10 * self._n

        self._edge_width = 0.02
        self._edge_line_width = self._edge_width / self._n * 400

    def _y_sq(self, r, c, b):

        return (
            numpy.array([[r + 0 + self._edge_width, r + 1 - self._edge_width], [r + 0, r + 1 - self._edge_width]]),
            numpy.array([[b + 0, b + 0], [b + 0, b + 0]]),
            numpy.array([[c + 0 + self._edge_width, c + 0 + self._edge_width],
                         [c + 1 - self._edge_width, c + 1 - self._edge_width]]),
        )

    def _z_sq(self, r, c, b):

        return (
            numpy.array([[c + 0 + self._edge_width, c + 0 + self._edge_width],
                         [c + 1 - self._edge_width, c + 1 - self._edge_width]]),
            numpy.array(
                [[r + 0 + self._edge_width, r + 1 - self._edge_width], [r + 0, r + 1 - self._edge_width]]),
            numpy.array([[b + 0, b + 0], [b + 0, b + 0]])
        )

    def _x_sq(self, r, c, b):

        return (
            numpy.array([[b + 0, b + 0], [b + 0, b + 0]]),
            numpy.array([[c + 0 + self._edge_width, c + 0 + self._edge_width],
                         [c + 1 - self._edge_width, c + 1 - self._edge_width]]),
            numpy.array([[r + 0 + self._edge_width, r + 1 - self._edge_width], [r + 0, r + 1 - self._edge_width]]))

    def _ax3d(self, fig, rectangle, edge_scale=1.0):

        ax = fig.add_axes(rectangle, projection='3d')

        ax.set_box_aspect([1, 1, 1])
        ax.axis("off")

        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')

        ax.set_xlim3d(0, self._n)
        ax.set_ylim3d(0, self._n)
        ax.set_zlim3d(0, self._n)

        state_6nn = self._state.reshape((6, self._n, self._n))

        tile_function = [lambda r, c: self._z_sq(self._n - 1 - r, c, self._n),
                         lambda r, c: self._z_sq(r, c, 0),
                         lambda r, c: self._y_sq(c, self._n - 1 - r, 0),
                         lambda r, c: self._y_sq(self._n - 1 - c, self._n - 1 - r, self._n),
                         lambda r, c: self._x_sq(self._n - 1 - r, c, self._n),
                         lambda r, c: self._x_sq(self._n - 1 - r, self._n - 1 - c, 0)]

        for f in range(6):
            for r in range(self._n):
                for c in range(self._n):
                    color = self._RGB[state_6nn[f, r, c]]

                    ax.plot_surface(*tile_function[f](r, c),
                                    color=color,
                                    edgecolor=self._EDGE_COLOR,
                                    shade=False, alpha=1,
                                    linewidth=self._edge_line_width * edge_scale,
                                    antialiased=True)

        return ax

    def _ax2d(self, fig, rectangle):

        ax = fig.add_axes(rectangle, frameon=False)
        ax.set_xticks([])
        ax.set_yticks([])

        d = 0.1 * self._n
        ax.set_xlim(0 - d, self._unfolded_grid.shape[1] + d)
        ax.set_ylim(0 - d, self._unfolded_grid.shape[0] + d)

        for r in range(self._unfolded_grid.shape[0]):
            for c in range(self._unfolded_grid.shape[1]):
                if self._unfolded_grid[r, c] >= 0:
                    ax.add_patch(Rectangle((c, self._unfolded_grid.shape[0] - 1 - r), 1, 1,
                                           linewidth=self._edge_line_width,
                                           ec=self._EDGE_COLOR,
                                           fc=self._RGB[self._state[self._unfolded_grid[r, c]]]))

        return ax

    def view3d(self):
        fig = plt.figure(figsize=(4, 4))
        self._ax3d(fig, (0, 0, 1, 1))
        return fig

    def view2d(self):
        fig = plt.figure(figsize=(4, 3))
        self._ax2d(fig, (0, 0, 1, 1))
        return fig

    def view(self):
        fig = plt.figure(figsize=(4, 3))
        self._ax2d(fig, (0, 0, 1, 1))
        self._ax3d(fig, (0.75 - 0.3 / 2, 0.015 + 0.15 - 0.25 / 2, 0.3, 0.25), 0.3)
        return fig


if __name__ == "__main__":
    c = MplRubikCube(2)

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

    c.view().savefig('5x5.png', dpi=200)
    c.view2d().savefig('5x51.png', dpi=200)
    c.view3d().savefig('5x52.png', dpi=200)

# State indices, face indices, orientation [U]P [D]OWN [F]RONT [B]ACK [L]EFT [R]IGHT:
#           0   1                                   0   0                                   U   U
#           2   3                                   0   0                                   U   U
#  20  21   8   9  16  17  12  13           5   5   2   2   4   4   3   3           L   L   F   F   R   R   B   B
#  22  23  10  11  18  19  14  15           5   5   2   2   4   4   3   3           L   L   F   F   R   R   B   B
#           4   5                                   1   1                                   D   D
#           6   7                                   1   1                                   D   D
#
#           W   W
#           W   W
#   O   O   G   G   R   R   B   B
#   O   O   G   G   R   R   B   B
#           Y   Y
#           Y   Y
