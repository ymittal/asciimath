# -*- coding: utf-8 -*-

from enum import Enum, unique
from collections import deque


@unique
class TokenClass(Enum):
    STRING = 0
    NUMBER = 1

    # grouping brackets
    LPAR = 100          # (
    RPAR = 101          # )
    LSQB = 102          # [
    RSQB = 103          # ]
    LBRA = 104          # {
    RBRA = 105          # }

    # relational symbols
    EQUALS = 200        # =
    LT = 201            # <
    LE = 202            # <=
    GT = 203            # >
    GE = 204            # >=
    NE = 205            # !=
    APPROX = 206        # ~~ (≈)
    IN = 207            # in (∈)
    NOTIN = 208         # !in (∉)
    SUBSET = 209        # sub (⊂)
    SUPSET = 210        # sup (⊃)
    SUBSETEQ = 211      # sube (⊆)
    SUPSETEQ = 212      # supe (⊇)
    CONGRUENCE = 213    # cong (≅)
    PROPORTIONAL = 214  # prop (∝)
    EQUIV = 215         # -= (≡)
    NOTSUBSET = 216
    NOTSUPSET = 217
    NOTSUBSETEQ = 218
    NOTSUPSETEQ = 219
    NOTEQUIV = 220      # !-= (≢)
    SIM = 221           # ~

    # logical symbols
    IMPLIES = 300       # =>
    IFF = 301           # <=>
    NOT = 302           # not (¬)
    FORALL = 303
    EXISTS = 304        # EE (∃)

    # operations
    PLUS = 400          # +
    MINUS = 401         # -
    CDOT = 402          # * (⋅)
    ASTERIX = 403       # ** (∗)
    DIV = 404           # / (\frac{}{})
    DIV_KG = 405        # -: (÷) kindergarten divide
    SUMMATION = 406     # sum (∑)
    PROD = 407          # prod (∏)
    CAP = 408           # cap (∩)
    CUP = 409           # cup (∪)
    WEDGE = 410         # ^^ (∧)
    VEE = 411           # vv (∨)
    TIMES = 412         # xx (×)
    SLASH = 413         # // (/)
    LIMIT = 414         # lim

    # Greek letters (caps end with '_C')
    ALPHA = 500
    BETA = 501
    GAMMA = 502
    DELTA = 503
    EPSILON = 504
    ETA = 505
    THETA = 506
    IOTA = 507
    KAPPA = 508
    LAMBDA = 509
    MU = 510
    NU = 511
    PI = 512
    RHO = 513
    SIGMA = 514
    TAU = 515
    UPSILON = 516
    PHI = 517
    VARPHI = 518
    CHI = 519
    PSI = 520
    OMEGA = 521
    VAREPSILON = 522
    VARTHETA = 523
    XI = 524

    GAMMA_C = 550
    DELTA_C = 551
    THETA_C = 552
    LAMBDA_C = 553
    PI_C = 554
    SIGMA_C = 555
    PHI_C = 556
    OMEGA_C = 557
    PSI_C = 558
    XI_C = 559

    # miscellaneous
    SQRT = 600
    ROOT = 601
    INTEGRAL = 602
    DEL = 603           # del (∂)
    GRAD = 604          # grad (∇)
    INF = 605
    ALEPH = 606
    SET_C = 607
    SET_N = 608
    SET_Q = 609
    SET_R = 610
    SET_Z = 611
    THEREFORE = 612     # :. (∴)
    BECAUSE = 613       # :' (∵)
    PLUSMINUS = 614
    OINT = 615          # oint (∮)
    FRAC = 616
    UNDERSCORE = 617
    CARAT = 618
    MINUSPLUS = 619
    COMMA = 620

    # arrows and accents
    RARR = 700          # rarr (->)
    LARR = 701          # larr (<-)
    LRARR = 702         # harr (<->)
    RARR_THICK = 703    # rArr (=>)
    LARR_THICK = 704    # lArr (<=)
    LRARR_THICK = 705   # hArr (<=>)
    UARR = 706          # uarr (↑)
    DARR = 707          # darr (↓)
    MAPSTO = 708        # |-> (↦)

    # standard functions
    SIN = 800
    COS = 801
    TAN = 802
    SEC = 803
    CSC = 804
    COT = 805
    ARCSIN = 806
    ARCCOS = 807
    ARCTAN = 808
    SINH = 809
    COSH = 810
    TANH = 811
    # SECH = 812
    # CSCH = 812
    # COTH = 813
    EXP = 814
    LOG = 815
    LN = 816
    DET = 817
    DIM = 818
    MOD = 819
    GCD = 820
    LCM = 821
    # LUB = 822
    # GLB = 823
    MIN = 824
    MAX = 825
    F = 826
    G = 827

    # multiline commands and matrices
    MULTILINE = 900
    END = 901
    CASES = 902
    SYSTEM = 903
    LINE_SEP = 904

    IF = 950
    BECAUSE = 951
    UNLESS = 952
    PROVIDED = 953
    OTHERWISE = 954

    EOF = 1000
    INVALID = 1001

    @staticmethod
    def _getWithin(start, end):
        res = []
        for token in TokenClass:
            if start <= token.value < end:
                res.append(token)
        return res

    @staticmethod
    def getGreekLetters():
        return TokenClass._getWithin(500, 600)

    @staticmethod
    def getConstants():
        res = []
        res.extend(TokenClass._getWithin(200, 500))
        res.extend(TokenClass._getWithin(600, 900))
        return res

    @staticmethod
    def getRelationalOps():
        return TokenClass._getWithin(200, 300)

    @staticmethod
    def getExplanations():
        return TokenClass._getWithin(950, 1000)


class Token:

    def __init__(self, tokenClass, data=None):
        assert tokenClass != None
        self.tokenClass = tokenClass
        self.data = data


class Tokenizer:

    STRING_TOKEN_MAP = {
        # operations
        'sum': TokenClass.SUMMATION,
        'prod': TokenClass.PROD,
        'lim': TokenClass.LIMIT,
        'nn': TokenClass.CAP,
        'uu': TokenClass.CUP,
        'vv': TokenClass.VEE,
        'xx': TokenClass.TIMES,

        # relational symbols
        'in': TokenClass.IN,
        'sub': TokenClass.SUBSET,
        'sup': TokenClass.SUPSET,
        'sube': TokenClass.SUBSETEQ,
        'supe': TokenClass.SUPSETEQ,
        'prop': TokenClass.PROPORTIONAL,

        # logical symbols
        'not': TokenClass.NOT,
        'AA': TokenClass.FORALL,
        'EE': TokenClass.EXISTS,

        # misc
        'sqrt': TokenClass.SQRT,
        'root': TokenClass.ROOT,
        'int': TokenClass.INTEGRAL,
        'oint': TokenClass.OINT,
        'del': TokenClass.DEL,
        'grad': TokenClass.GRAD,
        'oo': TokenClass.INF,
        'aleph': TokenClass.ALEPH,
        'CC': TokenClass.SET_C,
        'NN': TokenClass.SET_N,
        'QQ': TokenClass.SET_Q,
        'RR': TokenClass.SET_R,
        'ZZ': TokenClass.SET_Z,
        'frac': TokenClass.FRAC,

        # Greek letters
        'alpha': TokenClass.ALPHA,
        'beta': TokenClass.BETA,
        'gamma': TokenClass.GAMMA,
        'Gamma': TokenClass.GAMMA_C,
        'delta': TokenClass.DELTA,
        'Delta': TokenClass.DELTA_C,
        'epsilon': TokenClass.EPSILON,
        'varepsilon': TokenClass.VAREPSILON,
        'eta': TokenClass.ETA,
        'vartheta': TokenClass.VARTHETA,
        'theta': TokenClass.THETA,
        'Theta': TokenClass.THETA_C,
        'iota': TokenClass.IOTA,
        'kappa': TokenClass.KAPPA,
        'lambda': TokenClass.LAMBDA,
        'Lambda': TokenClass.LAMBDA_C,
        'mu': TokenClass.MU,
        'nu': TokenClass.NU,
        'xi': TokenClass.XI,
        'Xi': TokenClass.XI_C,
        'pi': TokenClass.PI,
        'Pi': TokenClass.PI_C,
        'rho': TokenClass.RHO,
        'sigma': TokenClass.SIGMA,
        'Sigma': TokenClass.SIGMA_C,
        'tau': TokenClass.TAU,
        'upsilon': TokenClass.UPSILON,
        'phi': TokenClass.PHI,
        'Phi': TokenClass.PHI_C,
        'varphi': TokenClass.VARPHI,
        'chi': TokenClass.CHI,
        'psi': TokenClass.PSI,
        'Psi': TokenClass.PSI_C,
        'omega': TokenClass.OMEGA,
        'Omega': TokenClass.OMEGA_C,

        # arrows and accents
        'uarr': TokenClass.UARR,
        'darr': TokenClass.DARR,
        'larr': TokenClass.LARR,
        'rarr': TokenClass.RARR,
        'harr': TokenClass.LRARR,
        'lArr': TokenClass.LARR_THICK,
        'rArr': TokenClass.RARR_THICK,
        'hArr': TokenClass.LRARR_THICK,

        # standard functions
        'sin': TokenClass.SIN,
        'cos': TokenClass.COS,
        'tan': TokenClass.TAN,
        'sec': TokenClass.SEC,
        'csc': TokenClass.CSC,
        'cot': TokenClass.COT,
        'arcsin': TokenClass.ARCSIN,
        'arccos': TokenClass.ARCCOS,
        'arctan': TokenClass.ARCTAN,
        'sinh': TokenClass.SINH,
        'cosh': TokenClass.COSH,
        'tanh': TokenClass.TANH,
        'exp': TokenClass.EXP,
        'log': TokenClass.LOG,
        'ln': TokenClass.LN,
        'det': TokenClass.DET,
        'dim': TokenClass.DIM,
        'mod': TokenClass.MOD,
        'gcd': TokenClass.GCD,
        'lcm': TokenClass.LCM,
        'min': TokenClass.MIN,
        'max': TokenClass.MAX,
        'f': TokenClass.F,
        'g': TokenClass.G,

        # multiline commands and matrices
        'multiline': TokenClass.MULTILINE,
        'end': TokenClass.END,
        'cases': TokenClass.CASES,
        'system': TokenClass.SYSTEM,

        'if': TokenClass.IF,
        'because': TokenClass.BECAUSE,
        'unless': TokenClass.UNLESS,
        'provided': TokenClass.PROVIDED,
        'otherwise': TokenClass.OTHERWISE
    }

    def __init__(self, scanner):
        self.sc = scanner
        self.charsBuffer = deque()

    def getStringToken(self, string):
        if string in Tokenizer.STRING_TOKEN_MAP:
            return Token(Tokenizer.STRING_TOKEN_MAP[string])

        for char in string:
            self.charsBuffer.append(Token(TokenClass.STRING, data=char))
        return self.charsBuffer.popleft()

    def nextToken(self):
        try:
            if len(self.charsBuffer):
                return self.charsBuffer.popleft()
            return self.next()
        except EOFError:
            return Token(TokenClass.EOF)

    def next(self):
        char = self.sc.next()
        if char is None:
            raise EOFError()
        elif char.isspace():
            return self.next()

        if char.isalpha():
            string = [char]
            while True:
                nextChar = self.sc.peek()
                if nextChar and nextChar.isalpha():
                    self.sc.next()
                    string.append(nextChar)
                else:
                    return self.getStringToken(''.join(string))

        if char.isdigit():
            # TODO: add support for decimals
            number = [char]
            while True:
                nextChar = self.sc.peek()
                if nextChar and nextChar.isdigit():
                    self.sc.next()
                    number.append(nextChar)
                else:
                    return Token(TokenClass.NUMBER,
                                 data=''.join(number))

        if char == '(':
            return Token(TokenClass.LPAR)

        elif char == '[':
            return Token(TokenClass.LSQB)

        elif char == '{':
            return Token(TokenClass.LBRA)

        elif char == ')':
            return Token(TokenClass.RPAR)

        elif char == ']':
            return Token(TokenClass.RSQB)

        elif char == '}':
            return Token(TokenClass.RBRA)

        elif char == ',':
            return Token(TokenClass.COMMA)

        elif char == ':':
            if self.sc.peek() == '.':
                self.sc.next()
                return Token(TokenClass.THEREFORE)
            elif self.sc.peek() == '\'':
                self.sc.next()
                return Token(TokenClass.BECAUSE)

        if char == '=':
            if self.sc.peek() == '>':
                self.sc.next()
                return Token(TokenClass.IMPLIES)
            return Token(TokenClass.EQUALS)

        elif char == '!':
            if self.sc.peek() == '=':
                self.sc.next()
                return Token(TokenClass.NE)
            elif self.sc.peek(length=2) == '-=':
                self.sc.next(length=2)
                return Token(TokenClass.NOTEQUIV)
            else:
                # TODO: fails when ! is followed by a token unaccounted for
                nextToken = self.nextToken()
                notTokensMap = {
                    TokenClass.IN: TokenClass.NOTIN,
                    TokenClass.SUBSET: TokenClass.NOTSUBSET,
                    TokenClass.SUPSET: TokenClass.NOTSUPSET,
                    TokenClass.SUBSETEQ: TokenClass.NOTSUBSETEQ,
                    TokenClass.SUPSETEQ: TokenClass.NOTSUPSETEQ
                }
                if nextToken.tokenClass in notTokensMap:
                    return Token(notTokensMap[nextToken.tokenClass])

        elif char == '<':
            if self.sc.peek() == '=':
                self.sc.next()
                if self.sc.peek() == '>':
                    self.sc.next()
                    return Token(TokenClass.IFF)
                return Token(TokenClass.LE)
            return Token(TokenClass.LT)

        elif char == '>':
            if self.sc.peek() == '=':
                self.sc.next()
                return Token(TokenClass.GE)
            return Token(TokenClass.GT)

        elif char == '~':
            if self.sc.peek() == '~':
                self.sc.next()
                return Token(TokenClass.APPROX)
            elif self.sc.peek() == '=':
                self.sc.next()
                return Token(TokenClass.CONGRUENCE)
            return Token(TokenClass.SIM)

        if char == '+':
            if self.sc.peek() == '-':
                self.sc.next()
                return Token(TokenClass.PLUSMINUS)
            return Token(TokenClass.PLUS)

        elif char == '-':
            if self.sc.peek() == ':':
                self.sc.next()
                return Token(TokenClass.DIV_KG)
            elif self.sc.peek() == '>':
                self.sc.next()
                return Token(TokenClass.RARR)
            elif self.sc.peek() == '=':
                self.sc.next()
                return Token(TokenClass.EQUIV)
            elif self.sc.peek() == '+':
                self.sc.next()
                return Token(TokenClass.MINUSPLUS)
            else:
                number = []
                while True:
                    nextChar = self.sc.peek()
                    if nextChar and nextChar.isdigit():
                        self.sc.next()
                        number.append(nextChar)
                    else:
                        break
                if number:
                    return Token(TokenClass.NUMBER,
                                 data='-' + ''.join(number))

            return Token(TokenClass.MINUS)

        elif char == '*':
            if self.sc.peek() == '*':
                self.sc.next()
                return Token(TokenClass.ASTERIX)
            return Token(TokenClass.CDOT)

        elif char == '/':
            if self.sc.peek() == '/':
                self.sc.next()
                return Token(TokenClass.SLASH)
            return Token(TokenClass.DIV)

        elif char == '^':
            if self.sc.peek() == '^':
                self.sc.next()
                return Token(TokenClass.WEDGE)
            return Token(TokenClass.CARAT)

        elif char == '_':
            return Token(TokenClass.UNDERSCORE)

        elif char == '|':
            if self.sc.peek(length=2) == '->':
                self.sc.next(length=2)
                return Token(TokenClass.MAPSTO)

        elif char == ';':
            if self.sc.peek() == ';':
                self.sc.next()
                return Token(TokenClass.LINE_SEP)

        return Token(TokenClass.INVALID, data=char)
