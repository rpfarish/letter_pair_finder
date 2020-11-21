from collections import deque


class Cube:

    def __init__(self):

        print('Instantiated Object')
        self.has_parity = False
        self.U = deque(['A', 'B', 'U', 'D'])
        self.L = deque(['E', 'F', 'G', 'H'])
        self.F = deque(['K', 'J', 'I', 'L'])
        self.R = deque(['M', 'N', 'O', 'P'])
        self.B = deque(['Z', 'R', 'S', 'T'])
        self.D = deque(['C', 'V', 'W', 'X'])
        self.all = self.U + self.L + self.F + self.R + self.B + self.D
        self.adj = {'A': 'Z', 'B': 'M', 'D': 'E', 'L': 'F', 'X': 'G', 'R': 'H', 'J': 'P', 'T': 'N', 'V': 'O', 'C': 'I',
                    'W': 'S', 'Z': 'A', 'M': 'B', 'E': 'D', 'F': 'L', 'G': 'X', 'H': 'R', 'P': 'J', 'N': 'T', 'O': 'V',
                    'I': 'C', 'S': 'W', 'U': 'K', 'K': None}
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

    def get_rotation(self, move):
        if move == "'":
            self.flip_parity()
            return -1
        elif move == '2':
            return 2
        elif move == '':
            self.flip_parity()
            return 1

    def flip_parity(self):
        self.has_parity = not self.has_parity

    def do_move(self, move: str):
        # todo check move is valid

        # get rotation
        rotation = self.get_rotation(move[1:])

        if move.startswith('U'):
            self._move_u(rotation)
        elif move.startswith('R'):
            self._move_r(rotation)
        elif move.startswith('L'):
            self._move_l(rotation)
        elif move.startswith('F'):
            self._move_f(rotation)
        elif move.startswith('B'):
            self._move_b(rotation)
        elif move.startswith('D'):
            self._move_d(rotation)

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
        # rotate adjacent of the R side
        s = deque([i[j] for i, j in zip(self.b_adj, self.b_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.b_adj):
            adjobj[self.b_iadj[n]] = s[n]

    def _move_d(self, rotation):
        self.D.rotate(rotation)
        # rotate adjacent of the R side
        s = deque([i[j] for i, j in zip(self.d_adj, self.d_iadj)])
        s.rotate(rotation)
        for n, adjobj in enumerate(self.d_adj):
            adjobj[self.d_iadj[n]] = s[n]

    @property
    def sides(self):
        return self.U + self.L + self.F + self.R + self.B + self.D

    @property
    def move_dict(self):
        # Todo make this dependent on parity for UF-UR swap
        return {default: current for default, current in zip(self.all, self.sides)}

    def display_cube(self):
        for i, name in zip([self.U, self.L, self.F, self.R, self.B, self.D], 'ULFRBD'):
            print('-------', name, '-------')
            print(f'   {i[0]}     ')
            print(f'{i[3]}     {i[1]}')
            print(f'   {i[2]}     \n')


c = Cube()

with open("scrambles.txt", "r") as f:
    scramble = f.readline()
    if '\n' in scramble:
        scramble = scramble.rstrip('\n')
    for move in scramble.split(' '):
        c.do_move(move)

c.display_cube()

print('scramle has parity', c.has_parity)


def memo_cube(buffer, move_dict):
    stack = [move_dict[buffer]]
    visited = []
    end = buffer  # what should end be?
    while stack:
        curr = stack.pop()
        if curr == end or c.adj[end] == curr:
            return visited
        if curr not in visited and c.adj[curr] not in visited :
            visited.append(curr)

        if (adj := move_dict[curr]) not in visited:
            stack.append(adj)


def pick_new_buffer(cube, visited):
    for next_buffer in cube.move_dict:
        if next_buffer not in visited and cube.adj[next_buffer] not in visited:
            return next_buffer
    else:
        return False


def do_memo(c):

    buffer = 'U'

    # todo find and delete flipped edges
    visit = memo_cube(buffer, c.move_dict)
    print(visit)
    # pick a new buffer
    visit.append(c.adj['U'])

    # ----- Cycle Break -----
    new_buffer = pick_new_buffer(c, visit)
    visit.append(new_buffer)

    sol = memo_cube(new_buffer, c.move_dict)
    if sol:
        print(new_buffer)
    print(sol, 2)
    visit.append(new_buffer)
    print(c.move_dict[sol[-1]], 7)

    #

    # ----- Cycle Break -----
    s = pick_new_buffer(c, visit)
    visit.append(s)

    sol = memo_cube(s, c.move_dict)
    if sol:
        print(s)
    print(sol, 4)
    print(c.move_dict[sol[-1]], 7)

    
try:
    do_memo(c)
except IndexError:
    pass

# # ----- Cycle Break -----
# new_buffer = pick_new_buffer(c, visit)
# visit.append(new_buffer)
#
# print(new_buffer, 5)
#
# sol = memo_cube(new_buffer, c.move_dict)
# print(sol, 6)
# print(c.move_dict[sol[-1]], 7)
# print()
#
# for nuffer in c.move_dict:
#     if nuffer not in visit and c.adj[nuffer] not in visit:
#         print(nuffer)

