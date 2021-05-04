import random
from collections import deque

from Cube.letterscheme import *


class Cube:
    def __init__(self, s):
        self.scramble = s.rstrip('\n').split(' ')
        self.faces = 'ULFRBD'

        self.default_edge_buffer = EDGE_BUFFER
        self.default_corner_buffer = CORNER_BUFFER
        self.edge_memo_buffers = set()
        self.corner_memo_buffers = None

        self.corner_buffer_order = [UBR, UBL, UFL, RDF, RDB, LDF, LDB]
        self.edge_buffer_order = [UB, UR, UL, DF, FR, FL, DR, DL]

        self.has_parity = not (len(self.scramble) - len(
            [move for move in self.scramble if move.endswith('2')])) % 2 == 0

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

        # UF-UR swap
        if self.has_parity:
            self.U_edges[1], self.U_edges[2] = self.U_edges[2], self.U_edges[1]
            self.F_edges[0], self.R_edges[0] = self.R_edges[0], self.F_edges[0]

        self.scramble_cube()

    def do_move(self, move: str):
        if not move:
            return
        rotations_map = {
            "'": -1,
            "2": 2,
            "": 1,
        }
        rotation = rotations_map.get(move[1:], 0)

        moves_map = {
            'U': (self.U_edges, self.u_adj_edges, self.u_adj_edges_index,
                  self.U_corners, self.u_adj_corners, self.u_adj_corners_index),

            'R': (self.R_edges, self.r_adj_edges, self.r_adj_edges_index,
                  self.R_corners, self.r_adj_corners, self.r_adj_corners_index),

            'L': (self.L_edges, self.l_adj_edges, self.l_adj_edges_index,
                  self.L_corners, self.l_adj_corners, self.l_adj_corners_index),

            'F': (self.F_edges, self.f_adj_edges, self.f_adj_edges_index,
                  self.F_corners, self.f_adj_corners, self.f_adj_corners_index),

            'B': (self.B_edges, self.b_adj_edges, self.b_adj_edges_index,
                  self.B_corners, self.b_adj_corners, self.b_adj_corners_index),

            'D': (self.D_edges, self.d_adj_edges, self.d_adj_edges_index,
                  self.D_corners, self.d_adj_corners, self.d_adj_corners_index),
        }

        side = moves_map.get(move[:1])
        self._rotate_layer(rotation, *side)

    @staticmethod
    def _rotate_layer(rotation, edges, adj_edges, adj_edges_index, corners, adj_corners, adj_corners_index):

        edges.rotate(rotation)
        corners.rotate(rotation)

        # rotate adjacent of the side edges
        side = deque([i[j] for i, j in zip(adj_edges, adj_edges_index)])
        side.rotate(rotation)
        for adj_side_obj, adj_edges_index, side_slice in zip(adj_edges, adj_edges_index, side):
            adj_side_obj[adj_edges_index] = side_slice

        # rotate adjacent of the side corners
        side = deque([(layer[i], layer[j]) for layer, (i, j) in zip(adj_corners, adj_corners_index)])
        side.rotate(rotation)
        for adj_side_obj, (i, j), (a, b) in zip(adj_corners, adj_corners_index, side):
            adj_side_obj[i] = a
            adj_side_obj[j] = b

    @property
    def solved_corners(self):
        return [default for default, current in zip(self.default_corners, self.all_corners)
                if default == current and default != self.default_corner_buffer
                and default not in self.adj_corners[self.default_corner_buffer]
                ]

    @property
    def twisted_corners(self):
        return {default: current for default, current in zip(self.default_corners, self.all_corners)
                if default in self.adj_corners[current] and default != self.default_corner_buffer
                and default not in self.adj_corners[self.default_corner_buffer]
                }

    @property
    def solved_edges(self):
        return [default for default, current in zip(self.default_edges, self.all_edges)
                if default == current and default != self.default_edge_buffer
                and default != self.adj_edges[self.default_edge_buffer]
                ]

    @property
    def flipped_edges(self):
        return {default: current for default, current in zip(self.default_edges, self.all_edges)
                if default == self.adj_edges[current] and default != self.default_edge_buffer
                and default != self.adj_edges[self.default_edge_buffer]
                }

    @property
    def all_edges(self):
        return self.U_edges + self.L_edges + self.F_edges + self.R_edges + self.B_edges + self.D_edges

    @property
    def all_edges_list(self):
        return [self.U_edges, self.L_edges, self.F_edges, self.R_edges, self.B_edges, self.D_edges]

    @property
    def all_corners(self):
        return self.U_corners + self.L_corners + self.F_corners + self.R_corners + self.B_corners + self.D_corners

    @property
    def all_corners_list(self):
        return [self.U_corners, self.L_corners, self.F_corners, self.R_corners, self.B_corners, self.D_corners]

    @property
    def edge_swaps(self):
        solved = self.solved_edges
        flipped = self.flipped_edges
        return {
            default: current
            for default, current in zip(self.default_edges, self.all_edges)
            if default not in solved and default not in flipped
        }

    @property
    def corner_swaps(self):
        solved = self.solved_corners
        twisted = self.twisted_corners
        return {
            default: current
            for default, current in zip(self.default_corners, self.all_corners)
            if current not in solved and current not in twisted
        }

    def cube_faces(self):
        return {face: pieces for face, *pieces in zip(self.faces, self.all_edges_list, self.all_corners_list)}

    def display_cube(self):
        for name, (e, c) in self.cube_faces().items():
            print('-------', name, '-------')
            print(f'      {c[0]} {e[0]} {c[1]}     ')
            print(f'      {e[3]}   {e[1]}          ')
            print(f'      {c[3]} {e[2]} {c[2]}   \n')

    def scramble_cube(self):
        for move in self.scramble:
            self.do_move(move)

    def edge_buffer_is_solved(self):
        return (self.U_edges[2] == self.default_edge_buffer
                and self.F_edges[0] == self.adj_edges[self.default_edge_buffer])

    def edge_buffer_is_flipped(self):
        return (self.U_edges[2] == self.adj_edges[self.default_edge_buffer]
                and self.F_edges[0] == self.default_edge_buffer)

    def is_solved(self):
        for key, value in self.edge_swaps.items():
            if key != value:
                return False
        else:
            return True

    def memo_corners(self):
        curr = buffer = self.default_corner_buffer
        moves = self.corner_swaps
        curr = moves[curr]
        memo = []
        while moves:
            new_memo = [curr]
            while True:
                curr = moves[curr]
                new_memo.append(curr)
                if curr == buffer or curr in self.adj_corners[buffer]:
                    break

            for i in new_memo:
                if i in moves:
                    moves.pop(i)
                    for j in self.adj_corners[i]:
                        moves.pop(j)
            else:
                if buffer in moves:
                    moves.pop(buffer)
                    for i in self.adj_corners[buffer]:
                        moves.pop(i)

            memo += new_memo

            if not moves:
                return [m for m in memo if m not in self.adj_corners[self.default_corner_buffer]
                        and m != self.default_corner_buffer]

            for new_buffer in self.corner_buffer_order:
                if new_buffer in moves:
                    curr = buffer = new_buffer
                    break
                curr = buffer = random.choice(list(moves))

    def memo_edges(self):
        buffer = self.default_edge_buffer
        avail_moves = self.edge_swaps
        def_buff = self.default_edge_buffer
        def_buff_adj = self.adj_edges[self.default_edge_buffer]
        curr = avail_moves[buffer]
        memo = []
        while avail_moves:
            new_memo = [curr]
            # Memo until a cycle break
            while True:
                curr = avail_moves[curr]
                if curr != self.default_edge_buffer and curr != self.adj_edges[self.default_edge_buffer]:
                    new_memo.append(curr)
                if curr == buffer or curr == self.adj_edges[buffer]:
                    break

            # Remove memo and adj from avail
            for move in new_memo:
                if move in avail_moves:
                    avail_moves.pop(move)
                    avail_moves.pop(self.adj_edges.get(move))

            # Remove buffer and adj from avail
            if buffer in avail_moves:
                avail_moves.pop(buffer)
                avail_moves.pop(self.adj_edges.get(buffer))

            # Append the new memo onto the current memo
            memo += new_memo

            # Return the the memo when avail is empty
            if not avail_moves:
                return [letter for letter in memo if letter != def_buff and letter != def_buff_adj]

            # Pick a new buffer
            for new_buffer in self.edge_buffer_order:
                if new_buffer in avail_moves:
                    curr = buffer = new_buffer
                    break
                curr = buffer = random.choice(list(avail_moves))

            self.edge_memo_buffers.add(buffer)

    @staticmethod
    def clean_edge_memo(memo):
        return ' '.join([f'{memo[i]}{memo[i + 1]}' for i in range(0, len(memo) - 1, 2)])
