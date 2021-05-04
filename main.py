"""Finds letter pairs from cube scrambles"""

from Cube.cube import Cube

# import database
# import ui_interface
scramble_file = "scrambles.txt"


def main():
    with open(scramble_file) as f:
        for number, scramble in enumerate(f.readlines()):
            cube = Cube(scramble)
            print("Solve Number:", number + 1)
            number += 1
            print(f'The scramble has{" no" * (not cube.has_parity)} parity')
            print(scramble)
            print("Edges:")
            print(cube.clean_edge_memo(cube.memo_edges()), cube.flipped_edges)
            print("Edge Buffers:")
            print(cube.edge_memo_buffers)
            print("Corners:")
            print(cube.memo_corners())
            print("Twisted Corners:")
            print(cube.twisted_corners, "\n")


# make ui
# todo finish importing database letter pairs

# todo create a context manager to add to each method

if __name__ == '__main__':
    main()
