import get_scrambles
from Cube.cube import Cube

all_corners = {
    "UBL", "UBR", "UFR", "UFL",
    "LUB", "LUF", "LDF", "LDB",
    "FUL", "FUR", "FDR", "FDL",
    "RUF", "RUB", "RDB", "RDF",
    "BUR", "BUL", "BDL", "BDR",
    "DFL", "DFR", "DBR", "DBL"
}

sticker_to_drill = "UBR"
adj1, adj2 = "RUB", "BUR"
all_corners.remove(sticker_to_drill)
all_corners.remove(adj1)
all_corners.remove(adj2)
algs_to_drill = {sticker_to_drill + i for i in all_corners}
number = 0

print('Running...')
strict = True
while True:
    scramble = get_scrambles.get_scramble()
    cube = Cube(scramble)
    corner_memo = cube.format_corner_memo(cube.memo_corners()).split(' ')
    no_cycle_break_corner_memo = set(corner_memo)

    if strict:
        no_cycle_break_corner_memo.clear()
        corner_buffers = cube.corner_memo_buffers
        for pair in corner_memo:
            print(pair)
            if len(pair) == 6:

                a = pair[:3]
                b = pair[3:]
            else:
                a = pair
                b = ''
            if a in corner_buffers or b in corner_buffers:
                break
            no_cycle_break_corner_memo.add(pair)
    if algs_to_drill.intersection(no_cycle_break_corner_memo):
        print(scramble)
        input()
