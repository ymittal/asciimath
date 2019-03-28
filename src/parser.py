#!/usr/bin/env python

from collections import deque

from ast import node
from scanner import Scanner
from tokenizer import Tokenizer, TokenClass
from utils import transform_environment


class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.buffer = deque()

        self.token = None
        self.consumeToken()

    def accept(self, *args):
        res = False
        for arg in args:
            res |= (self.token.tokenClass == arg)
        return res

    def consumeToken(self):
        if len(self.buffer):
            self.token = self.buffer.popleft()
        else:
            self.token = self.tokenizer.nextToken()
        # print(self.token.tokenClass)

    def lookAhead(self, k):
        assert k >= 1

        while len(self.buffer) < k:
            newToken = self.tokenizer.nextToken()
            self.buffer.append(newToken)

        return self.buffer[k - 1]

    def parseBinarySymbols(self):
        if self.accept(TokenClass.FRAC):
            self.consumeToken()
            numerator = self.parseSimpleExpr()
            denominator = self.parseSimpleExpr()
            return node.Frac(numerator, denominator)

        elif self.accept(TokenClass.ROOT):
            self.consumeToken()
            power = self.parseSimpleExpr()
            expr = self.parseSimpleExpr()
            return node.Root(power, expr)

    def _parseLines(self, separator):
        """Parse lines for multi-line commands (multiline,
        cases)
        :param separator line delimiter token
        :return list of lines, each containing a list of
            parsed expressions
        """
        lines = []
        currLine = []
        rhsSeen, explSeen = False, False
        while not self.accept(TokenClass.END):
            if self.accept(TokenClass.EOF):
                break

            if self.accept(separator.tokenClass):
                lines.append(currLine)
                self.consumeToken()
                currLine = []
                rhsSeen, explSeen = False, False
            elif (self.accept(*TokenClass.getRelationalOps())
                  and not rhsSeen and not explSeen):
                consClass = self.token.tokenClass
                self.consumeToken()
                rhsSeen = True
                currLine.extend([
                    node.MultipleLineCmd.RHS_BEGIN,
                    node.ConstantSymbol(consClass)
                ])
            elif (self.accept(*TokenClass.getExplanations())
                  and not explSeen):
                textClass = self.token.tokenClass
                self.consumeToken()
                explSeen = True
                currLine.extend([
                    node.MultipleLineCmd.EXPLAIN_BEGIN,
                    node.Text(textClass)
                ])
            else:
                expr = self.parseExpr()
                currLine.append(expr)
        self.consumeToken()
        return lines

    def parseMultiline(self):
        """Parse Multiline command
            multiline(sep) [[E]* relOp [E]* explan [E]* sep]* end
        """
        if self.accept(TokenClass.MULTILINE):
            self.consumeToken()
            if self.accept(TokenClass.LPAR):
                self.consumeToken()
                sep = self.token
                self.consumeToken()
                if self.accept(TokenClass.RPAR):
                    self.consumeToken()
                    lines = self._parseLines(sep)
                    return node.Multiline(lines)

    def parseCases(self):
        """Parses Cases command
            cases(sep) [[E]* explan [E]* sep]* end
        """
        if self.accept(TokenClass.CASES, TokenClass.SYSTEM):
            self.consumeToken()
            if self.accept(TokenClass.LPAR):
                self.consumeToken()
                sep = self.token
                self.consumeToken()
                if self.accept(TokenClass.RPAR):
                    self.consumeToken()
                    lines = self._parseLines(sep)
                    return node.Cases(lines)

    def parseSimpleExpr(self):
        if self.accept(TokenClass.SQRT):
            self.consumeToken()
            expr = self.parseSimpleExpr()
            return node.Sqrt(expr)

        elif self.accept(TokenClass.FRAC, TokenClass.ROOT):
            return self.parseBinarySymbols()

        elif self.accept(TokenClass.STRING):
            value = self.token.data
            self.consumeToken()
            return node.String(value)

        elif self.accept(TokenClass.NUMBER):
            value = self.token.data
            self.consumeToken()
            return node.Number(value)

        elif self.accept(*TokenClass.getGreekLetters()):
            letterClass = self.token.tokenClass
            self.consumeToken()
            return node.GreekLetter(letterClass)

        elif self.accept(*TokenClass.getConstants()):
            consClass = self.token.tokenClass
            self.consumeToken()
            return node.ConstantSymbol(consClass)

        elif self.accept(TokenClass.LPAR,
                         TokenClass.LSQB,
                         TokenClass.LBRA):
            lBracket = node.LeftBracket(self.token.tokenClass)
            self.consumeToken()
            exprs = self.parseCode()

            if self.accept(TokenClass.RPAR,
                           TokenClass.RSQB,
                           TokenClass.RBRA):
                rBracket = node.RightBracket(self.token.tokenClass)
                self.consumeToken()
                return node.BracketedExpr(exprs, lBracket, rBracket)

        elif self.accept(TokenClass.INVALID):
            value = self.token.data
            self.consumeToken()
            return node.Invalid(value)

    def _parseMatrixRow(self):
        if not self.accept(TokenClass.LSQB):
            return []

        self.consumeToken()
        row, cell = [], []
        while not self.accept(TokenClass.RSQB):
            if self.accept(TokenClass.EOF):
                break

            if self.accept(TokenClass.COMMA):
                self.consumeToken()
                row.append(node.ExprList(cell))
                cell = []
            else:
                expr = self.parseExpr()
                cell.append(expr)
        self.consumeToken()
        row.append(node.ExprList(cell))

        return row

    def parseIntermediateExpr(self):
        if self.accept(TokenClass.LSQB):
            if self.lookAhead(k=1).tokenClass == TokenClass.LSQB:
                self.consumeToken()
                matrix = []
                while not self.accept(TokenClass.RSQB):
                    if self.accept(TokenClass.EOF):
                        break

                    # parse rows, separated by commas
                    row = self._parseMatrixRow()
                    if self.accept(TokenClass.COMMA):
                        self.consumeToken()
                    matrix.append(row)

                self.consumeToken()
                return node.Matrix(data=matrix)

        simpleExpr1 = self.parseSimpleExpr()
        if self.accept(TokenClass.UNDERSCORE):
            self.consumeToken()
            simpleExpr2 = self.parseSimpleExpr()

            if self.accept(TokenClass.CARAT):
                self.consumeToken()
                simpleExpr3 = self.parseSimpleExpr()
                return node.SubSuperscriptExpr(simpleExpr1,
                                               simpleExpr2,
                                               simpleExpr3)

            return node.SubscriptExpr(simpleExpr1, simpleExpr2)

        elif self.accept(TokenClass.CARAT):
            self.consumeToken()
            simpleExpr2 = self.parseSimpleExpr()
            return node.SuperscriptExpr(simpleExpr1, simpleExpr2)

        return simpleExpr1

    def parseExpr(self):
        if self.accept(TokenClass.MULTILINE):
            return self.parseMultiline()

        elif self.accept(TokenClass.CASES, TokenClass.SYSTEM):
            return self.parseCases()

        imdExpr1 = self.parseIntermediateExpr()
        if self.accept(TokenClass.DIV):
            self.consumeToken()
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


def convertToLaTeX(string):
    string = transform_environment(string)
    tokenizer = Tokenizer(scanner=Scanner(string))
    parser = Parser(tokenizer=tokenizer)
    res = str(parser.parseCode())
    print(res)
    return res


if __name__ == '__main__':
    # string = '''cases(;;)x + y >= 2 otherwise;;end'''
    string = '[[2+3, 2^2], [3, 4^6], []]'
    string = '''
    sgn(x) = cases:
      1 if x > 0
        0 if x = 0
        -1
    '''
    preprocessed = transform_environment(string)
    print(convertToLaTeX(preprocessed))
