import random
from collections import deque


class Cube:
    def __init__(self, s, buffer='U'):
        self.scramble = s.rstrip('\n').split(' ')

        self.has_parity = not (len(self.scramble) - len(
            [move for move in self.scramble if move.endswith('2')])) % 2 == 0

        self.U_edges = deque(['A', 'B', 'U', 'D'])
        self.L_edges = deque(['E', 'F', 'G', 'H'])
        self.F_edges = deque(['K', 'J', 'I', 'L'])
        self.R_edges = deque(['M', 'N', 'O', 'P'])
        self.B_edges = deque(['Z', 'R', 'S', 'T'])
        self.D_edges = deque(['C', 'V', 'W', 'X'])
        self.original_edge_buffer = buffer
        self.orig_edges = self.U_edges + self.L_edges + self.F_edges + self.R_edges + self.B_edges + self.D_edges
        self.adj_edges = {'A': 'Z', 'B': 'M', 'D': 'E', 'L': 'F', 'X': 'G', 'R': 'H', 'J': 'P', 'T': 'N', 'V': 'O',
                          'C': 'I',
                          'W': 'S', 'Z': 'A', 'M': 'B', 'E': 'D', 'F': 'L', 'G': 'X', 'H': 'R', 'P': 'J', 'N': 'T',
                          'O': 'V',
                          'I': 'C', 'S': 'W', 'U': 'K', 'K': 'U'}

        self.u_adj_edges = [self.B_edges, self.R_edges, self.F_edges, self.L_edges]
        self.r_adj_edges = [self.U_edges, self.B_edges, self.D_edges, self.F_edges]
        self.l_adj_edges = [self.U_edges, self.F_edges, self.D_edges, self.B_edges]
        self.f_adj_edges = [self.U_edges, self.R_edges, self.D_edges, self.L_edges]
        self.b_adj_edges = [self.U_edges, self.L_edges, self.D_edges, self.R_edges]
        self.d_adj_edges = [self.F_edges, self.R_edges, self.B_edges, self.L_edges]

        self.u_edges_adj_index = [0, 0, 0, 0]
        self.r_edges_adj_index = [1, 3, 1, 1]
        self.l_edges_adj_index = [3, 3, 3, 1]
        self.f_edges_adj_index = [2, 3, 0, 1]
        self.b_edges_adj_index = [0, 3, 2, 1]
        self.d_edges_adj_index = [2, 2, 2, 2]

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
            'U': (self.U_edges, self.u_adj_edges, self.u_edges_adj_index),
            'R': (self.R_edges, self.r_adj_edges, self.r_edges_adj_index),
            'L': (self.L_edges, self.l_adj_edges, self.l_edges_adj_index),
            'F': (self.F_edges, self.f_adj_edges, self.f_edges_adj_index),
            'B': (self.B_edges, self.b_adj_edges, self.b_edges_adj_index),
            'D': (self.D_edges, self.d_adj_edges, self.d_edges_adj_index),
        }

        side = moves_map.get(move[:1])
        self._rotate_layer(rotation, *side)

    @staticmethod
    def _rotate_layer(rotation, face_edges, face_adj_edges, face_adj_index):
        face_edges.rotate(rotation)
        # rotate adjacent of the side edges
        side = deque([i[j] for i, j in zip(face_adj_edges, face_adj_index)])
        side.rotate(rotation)
        for adj_side_obj, adj_index, side_slice in zip(face_adj_edges, face_adj_index, side):
            adj_side_obj[adj_index] = side_slice

    @property
    def solved_edges(self):
        return [edge for edge, opp in zip(self.orig_edges, self.all_edges) if
                self.adj_edges[edge] == self.adj_edges[opp]
                and edge != self.original_edge_buffer and edge != self.adj_edges[self.original_edge_buffer]]

    @property
    def flipped_edges(self):
        return {edge: opp for edge, opp in zip(self.orig_edges, self.all_edges) if
                edge == self.adj_edges[opp] and edge != self.original_edge_buffer and edge != self.adj_edges[
                    self.original_edge_buffer]}

    @property
    def all_edges(self):
        return self.U_edges + self.L_edges + self.F_edges + self.R_edges + self.B_edges + self.D_edges

    @property
    def all_edges_list(self):
        return [self.U_edges, self.L_edges, self.F_edges, self.R_edges, self.B_edges, self.D_edges]

    @property
    def edge_swaps(self):
        solved = self.solved_edges
        flipped = self.flipped_edges
        return {
            default: current
            for default, current in zip(self.orig_edges, self.all_edges)
            if default not in solved and default not in flipped
        }

    def cube_faces(self):
        return {face: pieces for face, pieces in zip('ULFRBD', self.all_edges_list)}

    def display_cube(self):
        for name, e in self.cube_faces().items():
            print('-------', name, '-------')
            print(f'   {e[0]}     ')
            print(f'{e[3]}     {e[1]}')
            print(f'   {e[2]}     \n')

    def scramble_cube(self):
        for move in self.scramble:
            self.do_move(move)

    def edge_buffer_is_solved(self):
        return self.U_edges[2] == self.original_edge_buffer and self.F_edges[0] == self.adj_edges[
            self.original_edge_buffer]

    def edge_buffer_is_flipped(self):
        return self.U_edges[2] == self.adj_edges[self.original_edge_buffer] and self.F_edges[
            0] == self.original_edge_buffer

    def is_solved(self):
        for key, value in self.edge_swaps.items():
            if key != value:
                return False
        else:
            return True

    def memo_edges(self):
        curr = buffer = original_edge_buffer = self.original_edge_buffer
        moves = self.edge_swaps
        curr = moves[curr]
        memo = []
        while moves:
            new_memo = [curr]
            while True:
                curr = moves[curr]
                if curr != original_edge_buffer and curr != self.adj_edges[original_edge_buffer]:
                    new_memo.append(curr)
                if curr == buffer or curr == self.adj_edges[buffer]:
                    break

            for m in new_memo:
                try:
                    moves.pop(m)
                    moves.pop(self.adj_edges.get(m))
                except KeyError:
                    break
            else:
                try:
                    moves.pop(buffer)
                    moves.pop(self.adj_edges.get(buffer))
                except KeyError:
                    pass

            memo += new_memo

            if not moves:
                return [letter for letter in memo
                        if letter != self.original_edge_buffer
                        and letter != self.adj_edges[self.original_edge_buffer]]

            for new_buffer in ['A', 'B', 'D', 'C', 'W', 'J', 'L', 'V', 'X']:
                if new_buffer in moves:
                    curr = buffer = new_buffer
                    break
                curr = buffer = random.choice(list(moves))
            else:
                pass


def clean_edge_memo(memo):
    return ' '.join([f'{memo[i]}{memo[i + 1]}' for i in range(0, len(memo) - 1, 2)])


scramble_file = "scrambles.txt"

with open(scramble_file) as f:
    for number, scramble in enumerate(f.readlines()):
        cube = Cube(scramble)
        cube.display_cube()
        print(number + 1, scramble, end='')
        print(f'//the scramble has{" no" * (not cube.has_parity)} parity')
        print('//', clean_edge_memo(cube.memo_edges()), cube.flipped_edges, '\n')
