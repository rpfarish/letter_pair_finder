from collections import deque
from pprint import pprint
from random import choice


class Cube:
    def __init__(self, scramble):
        self.scramble = scramble.rstrip('\n').split(' ')

        self.has_parity = not (len(self.scramble) - len(
            [move for move in self.scramble if move.endswith('2')])) % 2 == 0

        self.U = deque(['A', 'B', 'U', 'D'])
        self.L = deque(['E', 'F', 'G', 'H'])
        self.F = deque(['K', 'J', 'I', 'L'])
        self.R = deque(['M', 'N', 'O', 'P'])
        self.B = deque(['Z', 'R', 'S', 'T'])
        self.D = deque(['C', 'V', 'W', 'X'])

        self.all = self.U + self.L + self.F + self.R + self.B + self.D
        self.adj = {'A': 'Z', 'B': 'M', 'D': 'E', 'L': 'F', 'X': 'G', 'R': 'H', 'J': 'P', 'T': 'N', 'V': 'O', 'C': 'I',
                    'W': 'S', 'Z': 'A', 'M': 'B', 'E': 'D', 'F': 'L', 'G': 'X', 'H': 'R', 'P': 'J', 'N': 'T', 'O': 'V',
                    'I': 'C', 'S': 'W', 'U': 'K', 'K': 'U'}

        self.u_adj = [self.B, self.R, self.F, self.L]
        self.r_adj = [self.U, self.B, self.D, self.F]
        self.l_adj = [self.U, self.F, self.D, self.B]
        self.f_adj = [self.U, self.R, self.D, self.L]
        self.b_adj = [self.U, self.L, self.D, self.R]
        self.d_adj = [self.F, self.R, self.B, self.L]

        self.u_iadj = [0, 0, 0, 0]
        self.r_iadj = [1, 3, 1, 1]
        self.l_iadj = [3, 3, 3, 1]
        self.f_iadj = [2, 3, 0, 1]
        self.b_iadj = [0, 3, 2, 1]
        self.d_iadj = [2, 2, 2, 2]

        if self.has_parity:
            self.U[1], self.U[2] = self.U[2], self.U[1]
            self.F[0], self.R[0] = self.R[0], self.F[0]

        self.scramble_cube()

    def do_move(self, move: str):
        rotations_map = {
            "'": -1,
            "2": 2,
            "": 1,
        }
        rotation = rotations_map.get(move[1:], 1)

        moves_map = {
            'U': self._move_u,
            'R': self._move_r,
            'L': self._move_l,
            'F': self._move_f,
            'B': self._move_b,
            'D': self._move_d,
        }

        moves_map.get(move[:1])(rotation)

    def _move_u(self, rotation):
        self.U.rotate(rotation)
        # rotate adjacent of the U side
        s = deque([i[j] for i, j in zip(self.u_adj, self.u_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.u_adj):
            adjobj[self.u_iadj[n]] = s[n]

    def _move_l(self, rotation):
        self.L.rotate(rotation)
        # rotate adjacent of the L side
        s = deque([i[j] for i, j in zip(self.l_adj, self.l_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.l_adj):
            adjobj[self.l_iadj[n]] = s[n]

    def _move_f(self, rotation):
        self.F.rotate(rotation)
        # rotate adjacent of the F side
        s = deque([i[j] for i, j in zip(self.f_adj, self.f_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.f_adj):
            adjobj[self.f_iadj[n]] = s[n]

    def _move_r(self, rotation):
        self.R.rotate(rotation)
        # rotate adjacent of the R side
        s = deque([i[j] for i, j in zip(self.r_adj, self.r_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.r_adj):
            adjobj[self.r_iadj[n]] = s[n]

    def _move_b(self, rotation):
        self.B.rotate(rotation)
        # rotate adjacent of the B side
        s = deque([i[j] for i, j in zip(self.b_adj, self.b_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.b_adj):
            adjobj[self.b_iadj[n]] = s[n]

    def _move_d(self, rotation):
        self.D.rotate(rotation)
        # rotate adjacent of the D side
        s = deque([i[j] for i, j in zip(self.d_adj, self.d_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.d_adj):
            adjobj[self.d_iadj[n]] = s[n]

    @property
    def solved_edges(self):
        return [edge for edge, opp in zip(self.all, self.sides) if
                self.adj[edge] == self.adj[opp] and edge != 'U' and edge != 'K']

    @property
    def flipped_edges(self):
        return {edge: opp for edge, opp in zip(self.all, self.sides) if
                edge == self.adj[opp] and edge != 'U' and edge != 'K'}

    @property
    def sides(self):
        return self.U + self.L + self.F + self.R + self.B + self.D

    @property
    def move_dict(self):
        solved = self.solved_edges
        flipped = self.flipped_edges
        return {
            default: current
            for default, current in zip(self.all, self.sides)
            if default not in solved and default not in flipped
        }

    def display_cube(self):
        for i, name in zip([self.U, self.L, self.F, self.R, self.B, self.D], 'ULFRBD'):
            print('-------', name, '-------')
            print(f'   {i[0]}     ')
            print(f'{i[3]}     {i[1]}')
            print(f'   {i[2]}     \n')

    def scramble_cube(self):
        for move in self.scramble:
            self.do_move(move)

    def buffer_is_solved(self):
        return self.U[2] == 'U' and self.F[0] == 'K'

    def buffer_is_flipped(self):
        return self.U[2] == 'K' and self.F[0] == 'B'

    def is_solved(self):
        for key, value in self.move_dict.items():
            if key != value:
                return False
        else:
            return True

    def memo(self):

        curr = buffer = original_buffer = 'U'
        moves = self.move_dict
        curr = moves[curr]

        memo = []
        while moves:
            new_memo = [curr]
            while True:
                curr = moves[curr]
                if curr != original_buffer and curr != self.adj[original_buffer]:
                    new_memo.append(curr)

                if curr == buffer or curr == self.adj[buffer]:
                    break

            for m in new_memo:
                try:
                    moves.pop(m)
                    moves.pop(self.adj.get(m))
                except KeyError:
                    break
            else:
                try:
                    moves.pop(buffer)
                    moves.pop(self.adj.get(buffer))
                except KeyError:
                    pass

            memo += new_memo

            if not moves:
                return [letter for letter in memo if letter != 'U' and letter != 'K']

            curr = buffer = choice(list(moves))


scramble_file = "scrambles.txt"

with open(scramble_file) as f:
    for number, scramble in enumerate(f.readlines()):
        c = Cube(scramble)
        print(number+1, scramble, end='')
        print(f'//the scramble has{" no" * (not c.has_parity)} parity')
        print('//',c.memo(), c.flipped_edges, '\n')

# c.display_cube()
#
# print(f'the scramble has{" no" * (not c.has_parity)} parity')
#
# pprint(c.move_dict)
#
# memo = c.memo()
#
# print(memo)

# curr = buffer = 'U'
# moves = c.move_dict
# curr = moves[curr]
#
# memo = []
# while moves:
#     new_memo = [curr]
#     while True:
#         curr = moves[curr]
#         print(curr)
#         if curr != 'U' and curr != c.adj['U']:
#             new_memo.append(curr)
#
#         if curr == buffer or curr == c.adj[buffer]:
#             break
#
#     print(new_memo, 'new_memo')
#     for m in new_memo:
#
#         try:
#             print('popping move', m)
#             moves.pop(m)
#             print('popping move adj', c.adj.get(m))
#             moves.pop(c.adj.get(m))
#         except KeyError:
#             break
#     else:
#         moves.pop(buffer)
#         moves.pop(c.adj.get(buffer))
#     memo += new_memo
#     print(memo, 'memo')
#
#     if not moves:
#         break
#     print(moves, 'moves')
#     curr = buffer = choice(list(moves))
#     print('new buffer', buffer)
#
