#!/usr/bin/env python

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

    def parseSimpleExpr(self):
        if self.accept(TokenClass.SQRT):
            self.nextToken()
            expr = self.parseSimpleExpr()
            return node.Sqrt(expr)

        elif self.accept(TokenClass.FRAC, TokenClass.ROOT):
            tokenClass = self.token.tokenClass
            self.nextToken()

            firstExpr = self.parseSimpleExpr()
            secondExpr = self.parseSimpleExpr()
            if tokenClass == TokenClass.FRAC:
                return node.Frac(firstExpr, secondExpr)
            else:
                return node.Root(firstExpr, secondExpr)

        elif self.accept(TokenClass.NUMBER):
            val = self.token.data
            self.nextToken()
            return node.Number(val)

# string = 'a !in B ** CC darr 2 = 2'
# tokenizer = Tokenizer(scanner=Scanner(string))
# while True:
#     token = tokenizer.nextToken()
#     if token.tokenClass == TokenClass.EOF:
#         break
#     elif token and token.data:
#         print token.tokenClass, ':', token.data
#     elif token:
#         print token.tokenClass

string = 'sqrt 3'
tokenizer = Tokenizer(scanner=Scanner(string))
parser = Parser(tokenizer=tokenizer)
print(parser.parseSimpleExpr())
