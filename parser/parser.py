#!/usr/bin/env python

import sys

from collections import deque

from scanner import Scanner
from tokenizer import Tokenizer, TokenClass
from ast import node


class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.buffer = deque()

        self.token = None
        self.nextToken()

    def accept(self, *args):
        res = False
        for arg in args:
            res |= (self.token.tokenClass == arg)
        return res

    def nextToken(self):
        if len(self.buffer):
            self.token = self.buffer.popleft()
        else:
            self.token = self.tokenizer.nextToken()

    def lookAhead(self, k):
        assert k >= 1

        while len(self.buffer) < k:
            newToken = self.tokenizer.nextToken()
            self.buffer.append(newToken)

        return self.buffer[k - 1]

    def parseBinarySymbols(self):
        if self.accept(TokenClass.FRAC):
            self.nextToken()
            numerator = self.parseSimpleExpr()
            denominator = self.parseSimpleExpr()
            return node.Frac(numerator, denominator)

        elif self.accept(TokenClass.ROOT):
            self.nextToken()
            power = self.parseSimpleExpr()
            expr = self.parseSimpleExpr()
            return node.Root(power, expr)

    def parseSimpleExpr(self):
        if self.accept(TokenClass.SQRT):
            self.nextToken()
            expr = self.parseSimpleExpr()
            return node.Sqrt(expr)

        elif self.accept(TokenClass.FRAC, TokenClass.ROOT):
            return self.parseBinarySymbols()

        elif self.accept(TokenClass.STRING):
            value = self.token.data
            self.nextToken()
            return node.String(value)

        elif self.accept(TokenClass.NUMBER):
            value = self.token.data
            self.nextToken()
            return node.Number(value)

        elif self.accept(*TokenClass.getGreekLetters()):
            letterClass = self.token.tokenClass
            self.nextToken()
            return node.GreekLetter(letterClass)

        elif self.accept(TokenClass.LPAR,
                         TokenClass.LSQB,
                         TokenClass.LBRA):
            leftBracket = node.LeftBracket(self.token.tokenClass)
            self.nextToken()
            exprs = self.parseCode()

            if self.accept(TokenClass.RPAR,
                           TokenClass.RSQB,
                           TokenClass.RBRA):
                rightBracket = node.RightBracket(self.token.tokenClass)
                self.nextToken()
                return node.BracketedExpr(exprs, leftBracket, rightBracket)

    def parseIntermediateExpr(self):
        simpleExpr1 = self.parseSimpleExpr()
        if self.accept(TokenClass.UNDERSCORE):
            self.nextToken()
            simpleExpr2 = self.parseSimpleExpr()

            if self.accept(TokenClass.CARAT):
                self.nextToken()
                simpleExpr3 = self.parseSimpleExpr()
                return node.SubSuperscriptExpr(simpleExpr1,
                                               simpleExpr2,
                                               simpleExpr3)

            return node.SubscriptExpr(simpleExpr1, simpleExpr2)

        elif self.accept(TokenClass.CARAT):
            self.nextToken()
            simpleExpr2 = self.parseSimpleExpr()
            return node.SuperscriptExpr(simpleExpr1, simpleExpr2)

        return simpleExpr1

    def parseExpr(self):
        imdExpr1 = self.parseIntermediateExpr()
        if self.accept(TokenClass.DIV):
            self.nextToken()
            imdExpr2 = self.parseIntermediateExpr()
            return node.Frac(imdExpr1, imdExpr2)

        return imdExpr1

    def parseCode(self):
        exprList = []
        expr = self.parseExpr()
        while expr is not None:
            exprList.append(expr)
            expr = self.parseExpr()
        return node.ExprList(exprList)


# string = 'a !in B ** CC darr2 = 2+3x'
# tokenizer = Tokenizer(scanner=Scanner(string))
# while True:
#     token = tokenizer.next:Token()
#     if token.tokenClass == TokenClass.EOF:
#         break
#     elif token and token.data:
#         print token.tokenClass, ':', token.data
#     elif token:
#         print token.tokenClass

string = '(2_alpha) a/b'
tokenizer = Tokenizer(scanner=Scanner(string))
parser = Parser(tokenizer=tokenizer)

print(parser.parseCode())
