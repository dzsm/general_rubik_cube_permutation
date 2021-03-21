import matplotlib.pyplot as plt
import numpy

from rubik_cube_permutation.mpl_rubik_cube import MplRubikCube, plt

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

#c.print_state().move('U R').print_state()
#c.reset().print_move('U', True)

#c.scramble(2, 0).print_state()
c.move('U F')
fig = c.view()
plt.show()
fig.savefig('2x2x2.png')

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
