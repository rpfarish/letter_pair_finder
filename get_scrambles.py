from pyTwistyScrambler import scrambler333


def get_scramble():
    return scrambler333.get_WCA_scramble()


def get_bld_scramble():
    return scrambler333.get_3BLD_scramble()


if __name__ == "__main__":
    print(get_bld_scramble())
