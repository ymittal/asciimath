#!/usr/bin/env python

from enum import Enum, unique


@unique
class TokenClass(Enum):
    CHAR = 0
    NUMBER = 1

    # grouping brackets
    LPAR = 100          # (
    RPAR = 101          # )
    LSQB = 102          # [
    RSQB = 103          # ]
    LBRA = 104          # {
    RBRA = 105          # }
    LPARCOLON = 106     # (:
    RPARCOLON = 107     # :)
    LBRACOLON = 108     # {:
    RBRACOLON = 109     # :}

    # relational symbols
    EQUALS = 200        # =
    LT = 201            # <
    LE = 202            # <=
    GT = 203            # >
    GE = 204            # >=
    NE = 205            # !=
    APPROX = 206        # ~~

    # logical symbols
    IMPLIES = 300       # =>
    IFF = 301           # <=>

    # operations
    PLUS = 400          # +
    MINUS = 401         # -
    CDOT = 402          # *
    ASTERIX = 403       # **
    DIV = 404           # /


class Token:

    def __init__(self, tokenClass, data=None):
        assert tokenClass != None
        self.tokenClass = tokenClass
        self.data = data


class Tokenizer:

    def __init__(self, scanner):
        self.sc = scanner

    def nextToken(self):
        try:
            return self.next()
        except EOFError:
            return

    def next(self):
        # if self.peek(length=2) in ['bb']:
        #     chars = self.next(length=2)
        #     if chars == 'bb':
        #         return Token(Token.BB)

        # elif self.peek(length=4) in ['sqrt',
        #                              'text',
        #                              'frac',
        #                              'root']:
        #     chars = self.next(length=4)
        #     if chars == 'sqrt':
        #         return Token(Token.SQRT)
        #     elif chars == 'text':
        #         return Token(Token.TEXT)
        #     elif chars == 'frac':
        #         return Token(Token.FRAC)
        #     elif chars == 'root':
        #         return Token(Token.ROOT)

        # elif self.peek(length=8) in ['stackrel']:
        #     chars = self.next(length=8)
        #     if chars == 'stackrel':
        #         return Token(Token.STACKREL)

        char = self.sc.next()
        if char is None:
            raise EOFError()
        elif char.isspace():
            return self.next()

        if char.isalpha():
            return Token(TokenClass.CHAR, data=char)

        if char.isdigit():
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
            if self.sc.peek() == ':':
                self.sc.next()
                return Token(TokenClass.LPARCOLON)
            return Token(TokenClass.LPAR)

        elif char == '[':
            return Token(TokenClass.LSQB)

        elif char == '{':
            if self.sc.peek() == ':':
                self.sc.next()
                return Token(TokenClass.LBRACOLON)
            return Token(TokenClass.LBRA)

        elif char == ')':
            return Token(TokenClass.RPAR)

        elif char == ']':
            return Token(Token.RSQB)

        elif char == '}':
            return Token(TokenClass.RBRA)

        elif char == ':':
            if self.sc.peek() == ')':
                self.sc.next()
                return Token(TokenClass.RPARCOLON)
            elif self.sc.peek() == '}':
                self.sc.next()
                return Token(TokenClass.RBRACOLON)

        if char == '=':
            if self.sc.peek() == '>':
                self.sc.next()
                return Token(TokenClass.IMPLIES)
            return Token(TokenClass.EQUALS)

        elif char == '!':
            if self.sc.peek() == '=':
                self.sc.next()
                return Token(TokenClass.NE)

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

        if char == '+':
            return Token(TokenClass.PLUS)

        elif char == '-':
            return Token(TokenClass.MINUS)

        elif char == '*':
            if self.sc.peek() == '*':
                self.sc.next()
                return Token(TokenClass.ASTERIX)
            return Token(TokenClass.CDOT)

        elif char == '/':
            return Token(TokenClass.DIV)
