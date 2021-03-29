"""Finds letter pairs from cube scrambles"""

from cube import Cube

# import database
# import ui_interface
scramble_file = "scrambles.txt"


# PATH = r"C:\Users\rpfar\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
# driver.get("https://cstimer.net")
# search = driver.find_element_by_id("scrambleDiv")
# dude = search.text.find("last/next scramble")
# scramble = search.text[526 + 18:].strip("\n")


# def foo():
#     search = driver.find_element_by_id("scrambleDiv")
#     scramble = search.text[526 + 18:].strip("\n")
#     return scramble


def main(scramble):
    number = 0
    while True:
        # with open(scramble_file) as f:
        #     for number, scramble in ((1, scr),):  # enumerate(f.readlines()):
        cube = Cube(scramble)
        # cube.display_cube()
        # pprint(cube.corner_swaps)
        print("Solve Number:", number + 1)
        number += 1
        print(scramble, end='')
        print(f'//The scramble has{" no" * (not cube.has_parity)} parity')
        print("Edges:")
        print('//', cube.clean_edge_memo(memo := cube.memo_edges()), cube.flipped_edges)
        # print(memo)
        print("Edge Buffers:")
        print(cube.edge_memo_buffers)
        print("Corners:")
        print(cube.memo_corners())
        print("Twisted Corners:")
        print(cube.twisted_corners, "\n")
        # print(cube.solved_corners)
        while True:
            # if scramble != foo():
            #     scramble = foo()
            #     break
            return


# make ui
# make database
# make todo list

# todo create a context manager to add to each method

if __name__ == '__main__':
    main("B L' F2 B2 R' U2 F2 B U R2 B' D2 F' U2 B' D2 F L2 D2")
    # pass
