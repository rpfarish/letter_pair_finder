from Cube.cube import Cube

cube = Cube(can_parity_swap=False)
print(cube.all_corners_list)
print(cube.all_edges_list)

corners = ['A', 'B', 'U', 'D', 'J', 'F', 'G', 'H', 'E', 'I', 'K', 'L', 'X', 'N', 'O', 'P', 'R', 'M', 'S', 'T', 'C', 'V',
           'W', 'Z']
edges = ['A', 'U', 'B', 'D', 'E', 'F', 'G', 'H', 'M', 'J', 'I', 'L', 'K', 'N', 'O', 'P', 'Z', 'R', 'S', 'T', 'C', 'V',
         'W', 'X']

# {'A': 'A', 'B': 'B', 'U': 'U', 'D': 'D', 'J': 'J', 'F': 'F', 'G': 'G', 'H': 'H', 'E': 'E', 'I': 'I', 'K': 'K', 'L': 'L', 'X': 'X', 'N': 'N', 'O': 'O', 'P': 'P', 'R': 'R', 'M': 'M', 'S': 'S', 'T': 'T', 'C': 'C', 'V': 'V', 'W': 'W', 'Z': 'Z'}
# {'A': 'A', 'U': 'U', 'B': 'B', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'M': 'M', 'J': 'J', 'I': 'I', 'L': 'L', 'K': 'K', 'N': 'N', 'O': 'O', 'P': 'P', 'Z': 'Z', 'R': 'R', 'S': 'S', 'T': 'T', 'C': 'C', 'V': 'V', 'W': 'W', 'X': 'X'}


# will need to convert letter memo (ABC) to side representation (UDFB)

# how to scramble the cube properly idk
# by swapping the pieces literally, manually by reassigning the location of the letters ?!

# HOW TO E.G.

# buffer = 'A'
# cycle_from_buffer = 'VL'

buffer = 'L'
cycle_from_buffer = 'VX'

edges = cube.edge_swaps
print(edges)
