from StringIO import StringIO
from collections import deque


class Scanner:

    def __init__(self, string):
        self.file = StringIO(string)

    def next(self, length=1):
        char = self.file.read(length)
        if char:
            return char
        else:
            raise EOFError()

    def peek(self, length=1):
        pos = self.file.tell()
        char = self.file.read(length)
        if not char:
            raise EOFError()
        self.file.seek(pos)
        return char


class Token:

    # TODO: use Enum
    ALPHA = 'alpha'
    NUMBER = 'num'

    LPAR = '('
    RPAR = ')'
    LSQB = '['
    RSQB = ']'
    LBRA = '{'
    RBRA = '}'
    LPARCOLON = '(:'
    RPARCOLON = ':)'
    LBRACOLON = '{:'
    RBRACOLON = ':}'

    def __init__(self, tokenType, arg=None):
        self.tokenType = tokenType
        self.arg = arg


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

        if char.isspace():
            return self.next()

        if char.isalpha():
            return Token(Token.ALPHA, arg=char)

        if char.isdigit():
            number = [char]
            while True:
                nextChar = self.peek()
                if nextChar and nextChar.isdigit():
                    self.next()
                    number.append(nextChar)
                else:
                    return Token(Token.NUMBER,
                                 arg=''.join(number))

        if char == '(':
            if self.sc.peek() == ':':
                self.sc.next()
                return Token(Token.LPARCOLON)
            return Token(Token.LPAR)

        elif char == '[':
            return Token(Token.LSQB)

        elif char == '{':
            if self.sc.peek() == ':':
                self.sc.next()
                return Token(Token.LBRACOLON)
            return Token(Token.LBRA)

        elif char == ')':
            return Token(Token.RPAR)

        elif char == ']':
            return Token(Token.RSQB)

        elif char == '}':
            return Token(Token.RBRA)

        elif char == ':':
            if self.sc.peek() == ')':
                self.sc.next()
                return Token(Token.RPARCOLON)
            elif self.sc.peek() == '}':
                self.sc.next()
                return Token(Token.RBRACOLON)


class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.buffer = deque()

    def nextToken(self):
        if len(self.buffer):
            return self.buffer.popleft()
        else:
            return self.tokenizer.nextToken()

    def lookAhead(self, k):
        assert k >= 1

        while len(self.buffer) < k:
            newToken = self.tokenizer.nextToken()
            self.buffer.append(newToken)

        return self.buffer[k - 1]


string = '( )()'
tokenizer = Tokenizer(scanner=Scanner(string))
while True:
    token = tokenizer.nextToken()
    if (token):
        print(token.tokenType)
    else:
        break
