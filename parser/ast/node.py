#!/usr/bin/env python

from tokenizer import TokenClass

# c ::= [a-zA-Z] | numbers | greek letters | standard functions | , | other symbols (see list)
# u ::= sqrt | text | bb | bbb | cc | tt | fr | sf | hat | bar | ul | vec | dot | ddot
# b ::= frac | root | stackrel
# l ::= ( | [ | {
# r ::= ) | ] | }
# S ::= c | l Code r | uS | bSS | "any text"
# I ::= S | S_S | S^S | S_S^S
# E ::= I | I/I
# Code ::= [ E ]


class ASTNode:

    @staticmethod
    def trimBrackets(expr):
        if isinstance(expr, BracketedExpr):
            return expr.exprs
        else:
            return expr


class Constant(ASTNode):
    pass


def _getGreekTokensToLaTeX():
    greekLetters = TokenClass.getGreekLetters()
    res = {}
    for letter in greekLetters:
        name = letter.name
        if name.endswith('_C'):
            name = name[:-2].capitalize()
        else:
            name = name.lower()
        res[letter] = '\\%s' % name

    return res


class GreekLetter(Constant):

    # TODO: add all letters
    TOKEN_CLASS_TO_LATEX = _getGreekTokensToLaTeX()

    def __init__(self, letterClass):
        self.letterClass = letterClass

    def __str__(self):
        return self.TOKEN_CLASS_TO_LATEX.get(self.letterClass, '')


class Number(Constant):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class String(Constant):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class UnarySymbol(ASTNode):

    def __init__(self, expr):
        self.expr = self.trimBrackets(expr)


class Sqrt(UnarySymbol):

    def __str__(self):
        return '\\sqrt{%s}' % str(self.expr)


class BinSymbol(ASTNode):

    def __init__(self, first, second):
        self.first = self.trimBrackets(first)
        self.second = self.trimBrackets(second)


class Root(BinSymbol):

    def __str__(self):
        return '\\sqrt[%s]{%s}' % (str(self.first),
                                   str(self.second))


class Frac(BinSymbol):

    def __str__(self):
        return '\\frac{%s}{%s}' % (str(self.first),
                                   str(self.second))


class Expr(ASTNode):
    pass


class BracketedExpr(Expr):

    def __init__(self, exprs, leftBracket, rightBracket):
        self.exprs = exprs
        self.leftBracket = leftBracket
        self.rightBracket = rightBracket

    def __str__(self):
        return ' %s%s%s ' % (str(self.leftBracket),
                             str(self.exprs),
                             str(self.rightBracket))


class SuperscriptExpr(Expr):

    def __init__(self, expr, power):
        self.expr = expr
        self.power = self.trimBrackets(power)

    def __str__(self):
        return '%s^{%s}' % (str(self.expr),
                            str(self.power))


class SubscriptExpr(Expr):

    def __init__(self, expr, sub):
        self.expr = expr
        self.sub = self.trimBrackets(sub)

    def __str__(self):
        return '%s_{%s}' % (str(self.expr),
                            str(self.sub))


class SubSuperscriptExpr(Expr):

    def __init__(self, expr, sub, sup):
        self.expr = expr
        self.sub = self.trimBrackets(sub)
        self.sup = self.trimBrackets(sup)

    def __str__(self):
        return '%s_{%s}^{%s}' % (str(self.expr),
                                 str(self.sub),
                                 str(self.sup))


class Bracket(ASTNode):

    def __init__(self, bracketClass):
        self.bracketClass = bracketClass


class LeftBracket(Bracket):

    TOKEN_CLASS_TO_LATEX = {
        TokenClass.LPAR: '\\left(',
        TokenClass.LSQB: '\\left[',
        TokenClass.LBRA: '\\left\\{'
    }

    def __str__(self):
        return self.TOKEN_CLASS_TO_LATEX.get(self.bracketClass, '')


class RightBracket(Bracket):

    TOKEN_CLASS_TO_LATEX = {
        TokenClass.RPAR: '\\right)',
        TokenClass.RSQB: '\\right]',
        TokenClass.RBRA: '\\right\\}'
    }

    def __str__(self):
        return self.TOKEN_CLASS_TO_LATEX.get(self.bracketClass, '')


class ExprList(ASTNode):

    def __init__(self, exprs):
        self.exprs = exprs

    def __str__(self):
        return ' '.join([str(e) for e in self.exprs])
