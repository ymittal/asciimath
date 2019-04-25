#!/usr/bin/env python

import utils
from src.tokenizer import TokenClass


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
        symbols = utils._getConstantSymbolsWithResizedBrackets()
        return self.tokenClass in symbols


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


class DeeVar(ASTNode):

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return 'd%s' % (str(self.var))


class Text(Constant):

    def __init__(self, tokenClass):
        self.tokenClass = tokenClass

    def __str__(self):
        return '\\text{%s }' % str(self.tokenClass.name.lower())


class UnaryOp(ASTNode):
    TO_LATEX = utils._getUnaryOpToLaTeX()

    def __init__(self, tokenClass, expr):
        self.tokenClass = tokenClass
        self.expr = self.stripBrackets(expr)

    def __str__(self):
        fmtStr = self.TO_LATEX.get(self.tokenClass, '{%s}')
        return fmtStr % str(self.expr)

    def resizeBrackets(self):
        return self.expr.resizeBrackets()


class InvertibleFunc(ASTNode):
    TO_LATEX = utils._getConstantSymbolsToLaTeX()

    def __init__(self, tokenClass, expr, power=None):
        self.tokenClass = tokenClass
        self.expr = self.stripBrackets(expr)
        self.power = self.stripBrackets(power)

    def __str__(self):
        funcStr = self.TO_LATEX.get(self.tokenClass, '')
        if self.power:
            return '%s^{%s} %s' % (funcStr,
                                   str(self.power),
                                   str(self.expr))
        else:
            return '%s\,%s' % (funcStr, str(self.expr))

    def resizeBrackets(self):
        return True if self.power else self.expr.resizeBrackets()


class LogFunc(InvertibleFunc):

    def __init__(self, tokenClass, expr, power=None, base=None):
        super(LogFunc, self).__init__(tokenClass, expr, power)
        self.base = self.stripBrackets(base)

    def __str__(self):
        baseStr = ''
        if self.base:
            baseStr = '_{%s}' % str(self.base)

        powerStr = '\,'
        if self.power:
            powerStr = '^{%s} ' % str(self.power)

        return '\\log%s%s%s' % (baseStr, powerStr,
                                str(self.expr))


class BinaryOp(ASTNode):

    def __init__(self, expr1, expr2):
        self.expr1 = self.stripBrackets(expr1)
        self.expr2 = self.stripBrackets(expr2)


class Root(BinaryOp):

    def __str__(self):
        return '\\sqrt[%s]{%s}' % (str(self.expr1),
                                   str(self.expr2))

    def resizeBrackets(self):
        return (self.expr1.resizeBrackets()
                or self.expr2.resizeBrackets())


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
        return '%s%s%s' % (self.lBracket.__str__(resize=resize),
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

    def __init__(self, lines):
        for line in lines:
            for idx, expr in enumerate(line):
                if expr == MultipleLineCmd.RHS_BEGIN:
                    line[idx] = String('&')
                elif expr == MultipleLineCmd.EXPLAIN_BEGIN:
                    line[idx] = String('&&')
        # map @param lines to ExprLists
        self.lines = map(lambda l: ExprList(l), lines)


class Multiline(MultipleLineCmd):

    def __str__(self):
        res = []
        for line in self.lines:
            res.append('\t' + str(line))

        if len(res) == 0:
            return '\\begin{align}\n\\end{align}'

        return '{}\n{}\n{}'.format('\\begin{align}',
                                   '\\\\\n'.join(res),
                                   '\\end{align}')


class Cases(MultipleLineCmd):

    def __str__(self):
        res = []
        for line in self.lines:
            res.append('\t' + str(line))

        if len(res) == 0:
            return '\\begin{cases}\n\\end{cases}'

        return '{}\n{}\n{}'.format('\\begin{cases}',
                                   '\\\\\n'.join(res),
                                   '\\end{cases}')


class Matrix(ASTNode):

    def __init__(self, data):
        self.data = data

    def __str__(self):
        res = []
        for row in self.data:
            rowStr = ' & '.join([str(c) for c in row])
            rowStr = '\t{}\\\\'.format(rowStr)
            res.append(rowStr)
        return '{}\n{}\n{}'.format('\\begin{bmatrix}',
                                   '\n'.join(res),
                                   '\\end{bmatrix}')


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
