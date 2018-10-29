#!/usr/bin/env python


class ASTNode:
    pass


class Number(ASTNode):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class UnarySymbol(ASTNode):

    def __init__(self, expr):
        self.expr = expr


class Sqrt(UnarySymbol):

    def __str__(self):
        return '\\sqrt{%s}' % str(self.expr)


class BinSymbol(ASTNode):

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Root(BinSymbol):

    def __str__(self):
        return '\\sqrt[%s]{%s}' % (str(self.first),
                                   str(self.second))


class Frac(BinSymbol):

    def __str__(self):
        return '\\frac{%s}{%s}' % (str(self.first),
                                   str(self.second))
