import get_scrambles
from Cube.cube import Cube

# algs_to_drill = {'EB', 'ZV', 'VZ', 'ZO', 'FA', 'SB', 'BV', 'CD', 'NM', 'AV', 'FL'}
algs_to_drill = {'AM'}
number = 0
print(len(algs_to_drill))
no_cycle_break_edge_memo = set()
print('Running...')
strict = False
while True:
    scramble = get_scrambles.get_scramble()
    cube = Cube(scramble)
    edge_memo = cube.format_edge_memo(cube.memo_edges()).split(' ')
    # print(scramble)
    no_cycle_break_edge_memo = set(edge_memo)

    if strict:
        # print(corner_buffers)
        no_cycle_break_edge_memo = set()
        edge_buffers = cube.edge_memo_buffers
        for pair in edge_memo:
            if len(pair) == 2:
                a, b = pair
            else:
                a = pair
                b = ''
            if a in edge_buffers or b in edge_buffers:
                break
            no_cycle_break_edge_memo.add(pair)

    # print("corner memo before cycle breaks", no_cycle_break_edge_memo)
    if algs_to_drill.intersection(no_cycle_break_edge_memo) or no_cycle_break_edge_memo.intersection(algs_to_drill):
        # print(algs_to_drill.intersection(no_cycle_break_edge_memo))
        print(scramble)
        # quit()
# D2 B2 L2 U2 B L2 F2 L2 B2 U' R' F' L' U2 F' L U B2 D
# D2 B2 L2 U2 B L2 F2 L2 B2 U' R' F' L' U2 F' L U B2 D
"""
D2 R2 F2 R2 F' U2 L2 U2 L2 U2 F' L' U' F R2 D2 R2 B2 L B U'
U' R2 B2 R2 U R2 F2 U B2 U' R2 L D B' F' L2 B' L F2 U2 F'
B2 D B2 D' B2 D L2 F2 L2 U2 R2 L' D2 B R F L2 B' U' B U
U B U2 B L2 F2 D2 R2 F' D2 F U B' R' U' L' B R D2
R2 F R2 D2 R2 U2 B F D2 R2 F' R' D2 U F L' D2 R D2 R'
L2 U' L2 R2 B2 L2 D' R2 U' B2 U' F' D' R2 B2 F2 R' U2 B U B
U F2 U' F2 L2 F2 R2 D' F2 U' R2 B R' B2 F D U2 L' R2 U' L
L R2 D L2 U' R2 B2 L2 D F2 L2 U B' R' F2 L D2 U F' R
F2 R2 B' D2 L2 R2 B' R2 F2 U2 F' R D2 F' U L D2 L2 F2 R' U
D2 L B' D' F2 R2 F U F B2 U2 R L D2 R F2 L2 D2 B2 L'
F' L2 F2 R2 B' U2 R2 B' L2 F L2 D' L' F2 D L B' D' L2
B' U2 L B2 F2 U2 R' D2 R2 D2 U2 L' F' D' R2 D2 U' F D' F' L'
L F L2 D' L2 U' R D2 R B' L2 F L2 B' D2 B' R2 U2 D2 R2
U B' D2 L2 R2 F U2 B F' R2 F' U2 R' F D F' U' L2 R' B'
B' D2 F2 L R2 U2 R D2 B2 L2 F2 R' B D2 B U L' B2 D' L U'
L2 D' B2 D2 B2 L2 D' B2 F2 L2 U2 B' U' L' R' D B U' R2 D2 R2
B' F2 R2 B2 D R2 D' L2 B2 R2 D2 B2 R B2 U' L' F' D F' R D'
U D F L2 U2 R B2 L D2 F B2 L2 F2 U F2 R2 B2 U' R2 L2 D'
R B2 D2 B2 L' D2 U2 R D2 L B2 F' U' R' U2 L2 D' B F2 R' D2
R2 U L2 F2 D2 R2 U' B2 L2 D' L2 B' R2 D R' B' D' L D2 F U2
B L2 F R2 F' L2 B2 R2 B2 F' R2 U F U L' F' R U L D' L'
L2 U' D F R U' F2 B' D R2 U2 R2 F' R2 F B2 R2 B D2
R' F D2 L' D' L2 U R' U2 B U D F2 L2 U' R2 B2 U B2 U
B2 D2 B2 U2 L B2 D2 R' D2 L R B D2 R' D2 B2 U R D R' B'
R2 D L2 B2 D' L2 D2 R2 B2 D' L U2 B2 U' B' L2 R F L R
B2 D L2 D2 R2 U' L2 B2 D' B2 U B' L' F2 U B U2 L D2 L2
U' F2 L2 F2 R2 U' R2 D' F' L D B' L2 B' F2 L2 B2 U2
L2 B2 F2 D' F2 D' U' B2 F2 L2 B L' B' F D U' F2 R D2 F'
D2 L2 U2 R' F2 L R U2 L' B2 F2 D F D2 F2 U R U2 L'
L2 U2 B2 R2 F L2 B D2 F2 R2 D2 U L R U L2 D' R' F D'
R D' B2 R2 D B R L' D2 R2 U' F2 D' R2 L2 D' F2 U F2
F' B2 D R2 B2 U' B2 F2 R2 F2 R2 D B R2 F2 D2 F' L2 F L'
D2 B' R2 B2 R2 F D2 L2 F' L2 F' L D2 R U' B2 U' F2 D2 R2
F' U F2 L2 D' R2 D2 R2 D' F2 R2 D' F L2 U' L B' L2 F2 D2 B
D2 B' D2 L' B' D' R' L' U' D2 F L2 B U2 F U2 D2 B2 R2 U2
D' L2 B2 L2 U F2 U' B2 F2 R2 D' L' D B F U' L' U R B R'
B' L2 D2 L2 B' U2 F L2 F2 R2 L' U R B F L D' R2 D2 R'
B2 D R' L2 D' R' F R2 B R U2 L U2 R F2 B2 U2 F2 L'
R L2 D2 F2 U' L2 U' F2 U L2 U2 R2 F' L2 F2 L B' L' D R F
D2 R U' F2 D' R U' F2 D' U2 R2 F R2 F D2 F' D2 L2 F2 D2
F L' U2 R2 U' L' D' L2 B' D2 B2 R' F2 B2 D2 F2 L U2 R
L' U L B' D F D L R2 D' R2 D2 F2 D R2 D F2 R2 B'
F2 U2 B' L2 F R2 D2 U2 B2 U2 R2 U R B' D L' F' U' F2 D2 F'
U' L2 B2 L2 B2 D U2 R2 D' R2 F' R2 U F' D2 L' R' B2 U' F'
F L2 R' F2 L' F2 D2 F2 L2 U2 R' U2 F' D2 B2 U' F' L F' R'
D' R2 U B2 L2 U' B2 F2 D B2 D2 F' R' B' L2 D F' L' R B' U2
"""
