import matplotlib.pyplot as plt
import numpy

from rubik_cube_permutation.mpl_rubik_cube import MplRubikCube, plt

c = MplRubikCube(4)

c.print_definition()

c.move('U F')
fig = c.view()
plt.show()
fig.savefig('4x4x4.png')
