import json
from pprint import pprint

from Cube import Cube
from solution import Solution

print("Please select an option")
# todo settings with buffer order and alt pseudo swaps for each parity alg
with open("settings.json") as f:
    settings = json.loads(f.read())
    letter_scheme = settings['letter_scheme']
    buffers = settings['buffers']
options = """
1. Memo the cube (optional letter scheme)
2. Drill list of algs
3. Drill sticker
4. Drill buffer
"""


# 5. Drill 3-twists


def memo_cube(scramble, letter_scheme, buffers):
    Solution(scramble, letter_scheme=letter_scheme).display()


def drill_list(piece_type):
    pass


def drill_sticker(piece_type, sticker, buffer=None, exclude=None):
    # todo specify some cycles you want to drill more than others
    if exclude is None:
        exclude = set()
    if piece_type == 'e':
        ls = letter_scheme if len(sticker) == 1 else None
        cycles_to_exclude = {sticker + piece for piece in exclude}
        sticker_scrambles = Cube(ls=ls).drill_edge_sticker(sticker, return_list=False,
                                                           cycles_to_exclude=cycles_to_exclude)
        print(sticker_scrambles)
    elif piece_type == 'c':
        ls = letter_scheme if len(sticker) == 1 else None
        cycles_to_exclude = {sticker + piece for piece in exclude}
        sticker_scrambles = Cube(ls=ls).drill_corner_sticker(sticker, return_list=False,
                                                           cycles_to_exclude=cycles_to_exclude)
        print(sticker_scrambles)
    else:
        print("sorry not a valid piece type")


def drill_buffer(piece_type, buffer=None):
    pass


import dlin

scramble = "F2 D2 R' D2 F2 R2 U2 B2 L2 R B' U' R F' D R U' B' D' L"
scramble = "U F2 U L2 F2 D' F2 D' L2 D' F2 U' R' D' B' D2 R' D' R B U'"

last_args = ""

while not (mode := input(options)).lower().startswith("q"):
    mode = int(mode)
    if mode == 1:
        scramble = input("please enter the scramble: ")
        if scramble == "!":
            scramble = last_args
            print(last_args)
        elif scramble == "!s":
            with open("scramble.txt") as f:
                scramble = f.readline().rstrip('\n').strip()
                print(scramble)
        if scramble == "":
            continue
        memo_cube(scramble, letter_scheme, buffers)
        last_args = scramble

        c = dlin.trace(scramble)
        pprint(c)
    elif mode == 2:
        piece_type = input("e for edges or c for corners: ")
        drill_list(piece_type)
    elif mode == 3:
        piece_type = input("e for edges or c for corners: ")
        args = input("sticker to drill (letter scheme or e.g. UR) (put to exclude after (must be same type)): ")
        if args == "!":
            args = last_args
            print(last_args)

        sticker, *exclude = args.upper().split()
        drill_sticker(piece_type, sticker, exclude=exclude)
        last_args = args

    elif mode == 4:
        piece_type = input("e for edges or c for corners: ")
        buffer = input("choose which buffer you want to drill put it in your letter scheme or like UR or UBL: ")
        drill_buffer(piece_type, buffer.upper())
    else:
        print("that option is not recognised")
