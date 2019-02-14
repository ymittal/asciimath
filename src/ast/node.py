#!/usr/bin/env python

import utils
from src.tokenizer import TokenClass


# c ::= [a-zA-Z] | numbers | greek letters | standard functions | , | other symbols (see list)
# u ::= sqrt
# b ::= frac | root
# l ::= ( | [ | {
# r ::= ) | ] | }
# S ::= c | l Code r | uS | bSS | multi | cases
# I ::= S | S_S | S^S | S_S^S
# E ::= I | I/I
# multi ::= multiline \(sep\) [[E] rel [E] explan [E] sep]* end
# cases ::= cases \(sep\) [[E] explan [E] sep]* end
# Code ::= [ E ]


class ASTNode(object):

    @staticmethod
    def stripBrackets(expr):
        if isinstance(expr, BracketedExpr):
            return expr.exprs
        else:
            return expr

    def resizeBrackets(self):
        return False


class Invalid(ASTNode):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class Constant(ASTNode):
    pass


class ConstantSymbol(Constant):

    TO_LATEX = utils._getConstantSymbolsToLaTeX()

    def __init__(self, tokenClass):
        self.tokenClass = tokenClass

    def __str__(self):
        return self.TO_LATEX.get(self.tokenClass, '')

    def resizeBrackets(self):
        return self.tokenClass in utils._getConstantSymbolsWithResizedBrackets()


class GreekLetter(Constant):

    TO_LATEX = utils._getGreekLettersToLaTeX()

    def __init__(self, tokenClass):
        self.tokenClass = tokenClass

    def __str__(self):
        return self.TO_LATEX.get(self.tokenClass, '')


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


class Text(Constant):

    def __init__(self, tokenClass):
        self.tokenClass = tokenClass

    def __str__(self):
        return '\\text{%s }' % str(self.tokenClass.name.lower())


class UnaryOp(ASTNode):

    def __init__(self, expr):
        self.expr = self.stripBrackets(expr)


class Sqrt(UnaryOp):

    def __str__(self):
        return '\\sqrt{%s}' % str(self.expr)

    def resizeBrackets(self):
        return self.expr.resizeBrackets()


class BinaryOp(ASTNode):

    def __init__(self, expr1, expr2):
        self.expr1 = self.stripBrackets(expr1)
        self.expr2 = self.stripBrackets(expr2)


class Root(BinaryOp):

    def __str__(self):
        return '\\sqrt[%s]{%s}' % (str(self.expr1),
                                   str(self.expr2))

    def resizeBrackets(self):
        return self.expr1.resizeBrackets() or self.expr2.resizeBrackets()


class Frac(BinaryOp):

    def __str__(self):
        return '\\frac{%s}{%s}' % (str(self.expr1),
                                   str(self.expr2))

    def resizeBrackets(self):
        return True


class Expr(ASTNode):
    pass


class BracketedExpr(Expr):

    def __init__(self, exprs, lBracket, rBracket):
        self.exprs = exprs
        self.lBracket = lBracket
        self.rBracket = rBracket

    def resizeBrackets(self):
        return self.exprs.resizeBrackets()

    def __str__(self):
        resize = self.resizeBrackets()
        return ' %s%s%s ' % (self.lBracket.__str__(resize=resize),
                             str(self.exprs),
                             self.rBracket.__str__(resize=resize))


class SuperscriptExpr(Expr):

    def __init__(self, expr, power):
        self.expr = expr
        self.power = self.stripBrackets(power)

    def __str__(self):
        return '%s^{%s}' % (str(self.expr),
                            str(self.power))

    def resizeBrackets(self):
        return True


class SubscriptExpr(Expr):

    def __init__(self, expr, sub):
        self.expr = expr
        self.sub = self.stripBrackets(sub)

    def __str__(self):
        return '%s_{%s}' % (str(self.expr),
                            str(self.sub))

    def resizeBrackets(self):
        return True


class SubSuperscriptExpr(Expr):

    def __init__(self, expr, sub, sup):
        self.expr = expr
        self.sub = self.stripBrackets(sub)
        self.sup = self.stripBrackets(sup)

    def __str__(self):
        return '%s_{%s}^{%s}' % (str(self.expr),
                                 str(self.sub),
                                 str(self.sup))

    def resizeBrackets(self):
        return True


class Bracket(ASTNode):

    def __init__(self, tokenClass):
        self.tokenClass = tokenClass


class LeftBracket(Bracket):

    TO_LATEX = {
        TokenClass.LPAR: ('\\left(', '('),
        TokenClass.LSQB: ('\\left[', '['),
        TokenClass.LBRA: ('\\left\\{', '\\{')
    }

    def __str__(self, resize=False):
        large, small = self.TO_LATEX.get(self.tokenClass, ('', ''))
        return large if resize else small


class RightBracket(Bracket):

    TO_LATEX = {
        TokenClass.RPAR: ('\\right)', ')'),
        TokenClass.RSQB: ('\\right]', ']'),
        TokenClass.RBRA: ('\\right\\}', '\\}')
    }

    def __str__(self, resize=False):
        large, small = self.TO_LATEX.get(self.tokenClass, ('', ''))
        return large if resize else small


class MultipleLineCmd(ASTNode):

    RHS_BEGIN = 'RHS_BEGIN'
    EXPLAIN_BEGIN = 'EXPLAIN_BEGIN'


class Multiline(MultipleLineCmd):

    def __init__(self, lines):
        for line in lines:
            for idx, expr in enumerate(line):
                if expr == MultipleLineCmd.RHS_BEGIN:
                    line[idx] = String('&')
                elif expr == MultipleLineCmd.EXPLAIN_BEGIN:
                    line[idx] = String('&&')
        # map @param lines to ExprLists
        self.lines = map(lambda l: ExprList(l), lines)

    def __str__(self):
        res = []
        for line in self.lines:
            res.append('\t{}\\\\'.format(str(line)))
        return '{}\n{}\n{}'.format('\\begin{align}',
                                   '\n'.join(res),
                                   '\\end{align}')


class Cases(MultipleLineCmd):

    def __init__(self, lines):
        self.lines = []
        for _l in lines:
            # remove RHS_BEGIN(s) from each line
            line = filter(lambda e: e != MultipleLineCmd.RHS_BEGIN, _l)
            for idx, expr in enumerate(line):
                if expr == MultipleLineCmd.EXPLAIN_BEGIN:
                    line[idx] = String('&&')
            self.lines.append(ExprList(line))

    def __str__(self):
        res = []
        for line in self.lines:
            res.append('\t{}\\\\'.format(str(line)))
        return '{}\n{}\n{}'.format('\\begin{cases}',
                                   '\n'.join(res),
                                   '\\end{cases}')


class ExprList(ASTNode):

    def __init__(self, exprs):
        self.exprs = exprs

    def __str__(self):
        return ' '.join([str(e) for e in self.exprs])

    def resizeBrackets(self):
        for expr in self.exprs:
            if expr.resizeBrackets():
                return True
        return False
