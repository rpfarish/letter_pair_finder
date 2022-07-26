import random
from collections import deque

import kociemba

from Cube.cube import Cube
from face_side_names import *
from get_scrambles import get_scramble

DEBUG = True


class ColoredCube(Cube):
    def __init__(self, s="", letterscheme='kociemba'):
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


def invert_solution(s: str) -> str:
    s = s.rstrip('\n').strip().split(' ')[:]
    inverse = []
    for move in reversed(s):
        if move.endswith("'"):
            inverse.append(move.strip("'"))
        elif move.endswith("2"):
            inverse.append(move)
        else:
            inverse.append(move + "'")
    return " ".join(inverse)


def cancel(pre_move, solution):
    # todo find a way to also cancel U D U moves
    # aka check for parallel cancelations
    solution = solution.rstrip('\n').strip().split(' ')[:]
    pre_move = pre_move.rstrip('\n').strip().split(' ')[:]
    rev_premove = pre_move[::-1]
    if DEBUG: print(solution, pre_move, rev_premove, sep=" || ")
    solved = ColoredCube()

    # full vs partial cancel

    # calculate cancel type
    for depth, (pre, s) in enumerate(zip(rev_premove.copy(), solution.copy())):
        combined = pre + " " + s
        canceled_cube = ColoredCube(combined)

        if DEBUG: print(pre, "||", s, "Full cancel:", "nope" if solved != canceled_cube else "yep")

        if not pre or not s:
            break

        if DEBUG: print(pre, "||", s, "Parital cancel:", "nope" if pre[0] != s[0] else "yep")

        if solved == canceled_cube and depth < 1:
            # full cancel
            # remove the two canceled moves and recurse
            if DEBUG: print('recursing')
            rev_premove.remove(pre)
            solution.remove(s)
            if DEBUG: print(solution, rev_premove, sep=" || ")

            return cancel(" ".join(rev_premove[::-1]), " ".join(solution))


        # partial cancel
        elif pre[0] == s[0] and depth < 1:
            canceled_cube = ColoredCube(pre + " " + s)
            kociemba_solution = invert_solution(kociemba.solve(canceled_cube.get_faces_colors())).split()
            if DEBUG: print('k sol', kociemba_solution)

            # kociemba_solution
            if DEBUG: print(rev_premove)
            rev_premove.remove(pre)
            solution.remove(s)
            solution = kociemba_solution + solution

    if DEBUG: print("Returning", " ".join(rev_premove[::-1]), " ".join(solution), sep=" || ")
    return " ".join(rev_premove[::-1]) + " " + " ".join(solution)
    # if partial cancel return simplified version


# if full cancel return removed full cancel and recurse


# def remove_cancellations(premove, sol):
#     sol = sol.rstrip('\n').strip().split(' ')[:]
#     premove = premove.rstrip('\n').strip().split(' ')[:]
#     rev_premove = premove[::-1]
#
#     if DEBUG: print(premove, sol)
#     d = ColoredCube(rev_premove[0] + " " + sol[0])
#     k = ColoredCube("")
#
#     first_moves_cancel = d == k
#
#     if first_moves_cancel:
#         rev_move = rev_premove.pop(0)
#         sol_move = sol.pop(0)
#         d = ColoredCube(rev_move + " " + sol_move)
#         sol = kociemba.solve(d.get_faces_colors()).split() + sol
#         print(sol)
#     for alfred, james in zip(rev_premove.copy(), sol.copy()):
#         d = ColoredCube(alfred + " " + james)
#         k = ColoredCube("")
#         if DEBUG: ("alf and james", alfred, "||", james)
#
#         if DEBUG: print(alfred[0], james[0])
#         # if moves cancel inversely
#         if d == k and first_moves_cancel:
#             if DEBUG: print("apparently the moves cancel", alfred, "||",  james)
#
#             rev_premove.remove(alfred)
#             sol.remove(james)
#
#         # if the moves cancel proportionally
#         elif alfred[0] == james[0] and first_moves_cancel:
#             if DEBUG: print("are you going to be good alf and james",  alfred, "||", james)
#             kociemba_solution = invert_solution(kociemba.solve(d.get_faces_colors())).split()
#             if DEBUG: print('k sol', kociemba_solution)
#
#             # kociemba_solution
#             if DEBUG: print(rev_premove)
#             rev_premove.remove(alfred)
#             sol.remove(james)
#             sol = kociemba_solution + sol
#             break
#         else:
#             if DEBUG: print("Neither condition was met")
#
#     return " ".join(rev_premove[::-1]) + " " + " ".join(sol)


# a = remove_cancellations("U F2 D", "U F' U B2 U' F R2")
# print(a)
# quit()


def has_cancellations(premove: list[str], sol: list[str]):
    if sol[0].startswith(premove[-1][0]):
        return True
    return False


def generate_premoves(scramble, min_len, max_len):
    premove_max_len = random.randint(min_len, max_len)
    premove_len = 0
    premoves = []
    premoves_faces = []
    faces = ['U', 'L', 'F', 'R', 'B', 'D']
    turns = ["", "'", "2"]
    scramble = scramble.split()
    a, b, *_ = scramble
    while premove_len < premove_max_len:
        face = random.choice(faces)
        # print(scramble)
        print(f"{face}, {a[0]}, {b[0]}, {premoves_faces}, {' '.join(scramble)}")
        print(face not in (a[0], b[0]), face not in premoves_faces)
        if face not in (a[0], b[0]) and face not in premoves_faces:
            turn = random.choice(turns)
            premoves.append(face + turn)
            premoves_faces.append(face)
            premove_len += 1

    return premoves


# solution = kociemba.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')
# print(solution)
# print(len('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'))

algs = [
    "R U R' U' R' F R2 U' R' U' R U R' F'",
    # "U R U R2' D' R U R' D R2 U2' R'",
    # "R' D' R U R' D R2 U' R' U R U R' U' R U R' U",
    # "U' R' U2 R U R2' D' R U R' D R2 U2'",
    # "U R U R' U R2 D R' U' R D' R' U' R'",
    # "R' D R' U R D' R' U R2 U' R2' U' R2 U'",
    # "U R' D' R U R' D R2 U R' U2 R U R' U'",
]

last_solution = None

while True:
    if not algs:
        break

    alg: str = random.choice(algs)
    # algs.remove(c)

    post_move = " ".join(get_scramble().split()[:random.randint(1, 3)])
    if DEBUG: print(post_move)

    alg += " " + post_move
    cube = ColoredCube(alg)
    k_sol = kociemba.solve(cube.get_faces_colors())

    if DEBUG: print("SETUP:", post_move, alg, sep=" || ")

    # DEBUGGING
    # post_move = "F D U2"
    # k_sol = "U2 D2 F U' F' D F U F2 R2 U2 R2 U' R2 U' R2 U'"
    print("//", post_move, "||", k_sol)
    # print("F D' F U' F' D F U F2 R2 U2 R2 U' R2 U' R2 U'", "---Expected")

    solution = cancel(post_move, k_sol)
    # if has_cancellations(post_move, k_sol):
    #     while True:
    #         post_move = get_scramble().split(" ")[:random.randint(1, 3)]
    #         post_move = " " + " ".join(post_move)
    #         c += post_move
    #         cube = ColoredCube(c)
    #         k_sol = kociemba.solve(cube.get_faces_colors())
    #         solution = post_move + " " + k_sol
    #         if not has_cancellations(post_move, k_sol) and ColoredCube(solution + " " + alg).is_solved():
    #             print(solution, "||", alg)
    #
    #             break

    if solution != last_solution:
        print(solution.strip())
        # print(k_solution.strip(), end="")
    if input() == 'quit':
        break
