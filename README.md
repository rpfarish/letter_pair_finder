# Letter Pair Finder

The repo allows you to quickly memorize Rubik's Cubes.
This also allows you to specify what cycles you would like to drill and
generates a scramble with those specific letter pairs in it.
Supports both edge and corner piece types though separately.
Does not account for breaking into twists, flips or parity shifting.
These scrambles are random move, but not random state but should be good enough for training
Please note that the letters on the buffers are not important, but each of them need to be unique.

## Features:

### Memo the cube

- to memorize the cube with these specific qualities: intelligent cycle breaking, memoing with alternate pseudoswaps,
  identifying: 2-flips, 2-twists, 3-twists, parity + twist, identifying floats, and trying to grade each of these
  solutions with some sort of metric and potentially identify 3-twist/2-twist + parity recommended solutions
- customizable lettering scheme for people who don't use Speffz

### Generate Training Scrambles

- Given a list of algs will generate random scrambles to drill those algs, and will print the alg if you forget it and
  keep track of how many and which ones it was
- Given a list of letter pairs (for either edges or corners) will generate random scrambles that have one or more of
  those letter pairs in a given scramble

- Working on drilling corners and edges and abstracting that logic
- I don't recommend going above 2 else it will take forever
- Given a sticker will let you drill all the cycles containing that sticker (forwards, backwards or both) by generating
  a random scramble that has one those letter pairs in a given scramble
- will let you repeat a certain sticker, letter pair or alg
- Generates a scramble with certain 2-flip, 2-twist, 3-twist, parity + twist
- Given buffer order will generate a scramble with just the cycles with that buffer scrambled

Most of this stuff is still wip.
