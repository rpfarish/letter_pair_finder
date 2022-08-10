"""Put your letter scheme here."""

# -------EDGES--------
# U Face
UB = 'A'
UR = 'B'
UF = 'U'
UL = 'D'

# L Face
LU = 'E'
LF = 'F'
LD = 'G'
LB = 'H'

# F Face
FU = 'K'
FR = 'J'
FD = 'I'
FL = 'L'

# R Face
RU = 'M'
RB = 'N'
RD = 'O'
RF = 'P'

# B Face
BU = 'Z'
BL = 'R'
BD = 'S'
BR = 'T'

# D Face
DF = 'C'
DR = 'V'
DB = 'W'
DL = 'X'

# -------CORNERS--------

# U Face
UBL = 'A'
UBR = 'B'
UFR = 'U'
UFL = 'D'

# L Face
LUB = 'J'
LUF = 'F'
LDF = 'G'
LDB = 'H'

# F Face
FUL = 'E'
FUR = 'I'
FDR = 'K'
FDL = 'L'

# R Face
RUF = 'X'
RUB = 'N'
RDB = 'O'
RDF = 'P'

# B Face
BUR = 'R'
BUL = 'M'
BDL = 'S'
BDR = 'T'

# D Face
DFL = 'C'
DFR = 'V'
DBR = 'W'
DBL = 'Z'

letter_scheme = dict(
    # U Face
    UB='A',
    UR='B',
    UF='U',
    UL='D',

    # L Face
    LU='E',
    LF='F',
    LD='G',
    LB='H',

    # F Face
    FU='K',
    FR='J',
    FD='I',
    FL='L',

    # R Face
    RU='M',
    RB='N',
    RD='O',
    RF='P',

    # B Face
    BU='Z',
    BL='R',
    BD='S',
    BR='T',

    # D Face
    DF='C',
    DR='V',
    DB='W',
    DL='X',

    # -------CORNERS--------

    # U Face
    UBL='A',
    UBR='B',
    UFR='U',
    UFL='D',

    # L Face
    LUB='J',
    LUF='F',
    LDF='G',
    LDB='H',

    # F Face
    FUL='E',
    FUR='I',
    FDR='K',
    FDL='L',

    # R Face
    RUF='X',
    RUB='N',
    RDB='O',
    RDF='P',

    # B Face
    BUR='R',
    BUL='M',
    BDL='S',
    BDR='T',

    # D Face
    DFL='C',
    DFR='V',
    DBR='W',
    DBL='Z',
)


# -----BUFFERS------
# EDGE_BUFFER = UF
# CORNER_BUFFER = UFR


class PieceId:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        self.face = self.pos[0]

    def __repr__(self):
        return self.pos

    def __add__(self, other):
        return self.pos + other.pos


class LetterScheme:

    def __init__(self, ltr_scheme=None):
        if ltr_scheme is None:
            ltr_scheme = letter_scheme

        # initialize scheme to null so IDE won't flag as missing property
        self.UB = ''
        self.UR = ''
        self.UF = ''
        self.UL = ''
        self.LU = ''
        self.LF = ''
        self.LD = ''
        self.LB = ''
        self.FU = ''
        self.FR = ''
        self.FD = ''
        self.FL = ''
        self.RU = ''
        self.RB = ''
        self.RD = ''
        self.RF = ''
        self.BU = ''
        self.BL = ''
        self.BD = ''
        self.BR = ''
        self.DF = ''
        self.DR = ''
        self.DB = ''
        self.DL = ''
        self.UBL = ''
        self.UBR = ''
        self.UFR = ''
        self.UFL = ''
        self.LUB = ''
        self.LUF = ''
        self.LDF = ''
        self.LDB = ''
        self.FUL = ''
        self.FUR = ''
        self.FDR = ''
        self.FDL = ''
        self.RUF = ''
        self.RUB = ''
        self.RDB = ''
        self.RDF = ''
        self.BUR = ''
        self.BUL = ''
        self.BDL = ''
        self.BDR = ''
        self.DFL = ''
        self.DFR = ''
        self.DBR = ''
        self.DBL = ''

        for pos, name in ltr_scheme.items():
            setattr(self, pos, PieceId(pos, name))


if __name__ == '__main__':
    scheme = LetterScheme(letter_scheme)
    # print(dir(scheme))
    # print(scheme.BD)
