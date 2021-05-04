import random
from collections import deque

import kociemba

from Cube.cube import Cube
from face_side_names import *


def invert_solution(solution):
    solution = solution.rstrip('\n').strip().split(' ')[:]
    inverse = []
    for move in reversed(solution):
        if move.endswith("'"):
            inverse.append(move.strip("'"))
        elif move.endswith("2"):
            inverse.append(move)
        else:
            inverse.append(move + "'")
    return " ".join(inverse)


class ColoredCube(Cube):
    def __init__(self, s, letterscheme='kociemba'):
        self.scramble = s.rstrip('\n').strip().split(' ')[:]
        self.faces = "ULFRBD"
        self.kociemba_order = "URFDLB"

        self.default_edge_buffer = EDGE_BUFFER
        self.default_corner_buffer = CORNER_BUFFER
        self.edge_memo_buffers = set()
        self.corner_memo_buffers = set()

        self.corner_buffer_order = [UBR, UBL, UFL, RDF, RDB, LDF, LDB]
        self.edge_buffer_order = [UB, UR, UL, DF, FR, FL, DR, DL]

        double_turns = [move for move in self.scramble if move.endswith('2')]
        self.has_parity = (len(self.scramble) - len(double_turns)) % 2 == 1

        self.U_corners = deque([UBL, UBR, UFR, UFL])
        self.L_corners = deque([LUB, LUF, LDF, LDB])
        self.F_corners = deque([FUL, FUR, FDR, FDL])
        self.R_corners = deque([RUF, RUB, RDB, RDF])
        self.B_corners = deque([BUR, BUL, BDL, BDR])
        self.D_corners = deque([DFL, DFR, DBR, DBL])

        self.U_edges = deque([UB, UR, UF, UL])
        self.L_edges = deque([LU, LF, LD, LB])
        self.F_edges = deque([FU, FR, FD, FL])
        self.R_edges = deque([RU, RB, RD, RF])
        self.B_edges = deque([BU, BL, BD, BR])
        self.D_edges = deque([DF, DR, DB, DL])

        self.default_edges = self.U_edges + self.L_edges + self.F_edges + self.R_edges + self.B_edges + self.D_edges
        self.default_corners = self.U_corners + self.L_corners + self.F_corners + self.R_corners + self.B_corners + self.D_corners
        self.adj_edges = {
            UB: BU, UR: RU, UL: LU, FL: LF, DL: LD,
            BL: LB, FR: RF, BR: RB, DR: RD, DF: FD,
            DB: BD, BU: UB, RU: UR, LU: UL, LF: FL,
            LD: DL, LB: BL, RF: FR, RB: BR, RD: DR,
            FD: DF, BD: DB, UF: FU, FU: UF
        }

        self.adj_corners = {
            UBL: BUL + LUB, UBR: RUB + BUR, UFR: FUR + RUF, UFL: LUF + FUL,
            LUB: UBL + BUL, LUF: FUL + UFL, LDF: DFL + FDL, LDB: BDL + DBL,
            FUL: UFL + LUF, FUR: RUF + UFR, FDR: DFR + RDF, FDL: LDF + DFL,
            RUF: UFR + FUR, RUB: BUR + UBR, RDB: DBR + BDR, RDF: FDR + DFR,
            BUR: UBR + RUB, BUL: LUB + UBL, BDL: DBL + LDB, BDR: RDB + DBR,
            DFL: FDL + LDF, DFR: RDF + FDR, DBR: BDR + RDB, DBL: LDB + BDL
        }

        self.u_adj_edges = [self.B_edges, self.R_edges, self.F_edges, self.L_edges]
        self.r_adj_edges = [self.U_edges, self.B_edges, self.D_edges, self.F_edges]
        self.l_adj_edges = [self.U_edges, self.F_edges, self.D_edges, self.B_edges]
        self.f_adj_edges = [self.U_edges, self.R_edges, self.D_edges, self.L_edges]
        self.b_adj_edges = [self.U_edges, self.L_edges, self.D_edges, self.R_edges]
        self.d_adj_edges = [self.F_edges, self.R_edges, self.B_edges, self.L_edges]

        self.u_adj_corners = [self.B_corners, self.R_corners, self.F_corners, self.L_corners]
        self.r_adj_corners = [self.U_corners, self.B_corners, self.D_corners, self.F_corners]
        self.l_adj_corners = [self.U_corners, self.F_corners, self.D_corners, self.B_corners]
        self.f_adj_corners = [self.U_corners, self.R_corners, self.D_corners, self.L_corners]
        self.b_adj_corners = [self.U_corners, self.L_corners, self.D_corners, self.R_corners]
        self.d_adj_corners = [self.F_corners, self.R_corners, self.B_corners, self.L_corners]

        self.u_adj_corners_index = [(1, 0), (1, 0), (1, 0), (1, 0)]
        self.r_adj_corners_index = [(2, 1), (0, 3), (2, 1), (2, 1)]
        self.l_adj_corners_index = [(0, 3), (0, 3), (0, 3), (2, 1)]
        self.f_adj_corners_index = [(3, 2), (0, 3), (1, 0), (2, 1)]
        self.b_adj_corners_index = [(1, 0), (0, 3), (3, 2), (2, 1)]
        self.d_adj_corners_index = [(3, 2), (3, 2), (3, 2), (3, 2)]

        self.u_adj_edges_index = [0, 0, 0, 0]
        self.r_adj_edges_index = [1, 3, 1, 1]
        self.l_adj_edges_index = [3, 3, 3, 1]
        self.f_adj_edges_index = [2, 3, 0, 1]
        self.b_adj_edges_index = [0, 3, 2, 1]
        self.d_adj_edges_index = [2, 2, 2, 2]

        self.scramble_cube()

    def get_faces_colors(self):
        cube_faces = self.cube_faces()
        cube_string = ""
        for face_name in self.kociemba_order:
            e, c = cube_faces.get(face_name)
            face = c[0] + e[0] + c[1]
            face += e[3] + face_name + e[1]
            face += c[3] + e[2] + c[2]
            cube_string += face
        return cube_string

    def display_cube(self):
        for name, (e, c) in self.cube_faces().items():
            print('-------', name, '-------')
            print(f'      {c[0]} {e[0]} {c[1]}     ')
            print(f'      {e[3]} {name} {e[1]}     ')
            print(f'      {c[3]} {e[2]} {c[2]}   \n')


ud_stickers = ["UBL", "UBR", "UFL", "DFL", "DFR", "DBR", "DBL"]
orientation = ["CW", "CCW"]

# solution = kociemba.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')
# print(solution)
# print(len('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'))
cw_twists = {
    "UBL": "R U R D R' D' R D R' U' R D' R' D R D' R2",
    "UBR": "R D R' D' R D R' U' R D' R' D R D' R' U",
    "UFL": "U' R' D R D' R' D R U R' D' R D R' D' R",
    "DFL": "U R U' R' D R U R' U' R U R' D' R U' R'",
    "DFR": "D' U' R' D R U R' D' R D R' D' R U' R' D R U",
    "DBR": "U R U' R' D' R U R' U' R U R' D R U' R'",
    "DBL": "D' R D R' U' R D' R' D R D' R' U R D R'"
}

ccw_twist = {
    "UBL": "R2 D R' D' R D R' U R D' R' D R D' R' U' R'",
    "UBR": "U' R D R' D' R D R' U R D' R' D R D' R'",
    "UFL": "R' D R D' R' D R U' R' D' R D R' D' R U",
    "DFL": "R U R' D R U' R' U R U' R' D' R U R' U'",
    "DFR": "U' R' D' R U R' D R D' R' D R U' R' D' R U D",
    "DBR": "R U R' D' R U' R' U R U' R' D R U R' U'",
    "DBL": "R D' R' U' R D R' D' R D R' U R D' R' D",
}

last_solution = None
while True:
    corner1, corner2 = random.sample(ud_stickers, k=2)
    twists = cw_twists[corner1] + " " + cw_twists[corner2]
    cube = ColoredCube(twists)
    solution = kociemba.solve(cube.get_faces_colors())
    if solution != last_solution:
        print(solution, end="")
        last_solution = solution
    if input() == 'quit':
        break
