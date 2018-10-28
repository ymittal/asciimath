from StringIO import StringIO
from collections import deque

from tokenizer import Tokenizer


class Scanner:

    def __init__(self, string):
        self.file = StringIO(string)

    def next(self, length=1):
        char = self.file.read(length)
        if char:
            return char
        else:
            return None

    def peek(self, length=1):
        pos = self.file.tell()
        char = self.file.read(length)
        if not char:
            return None
        self.file.seek(pos)
        return char


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


string = 'a>=b**c'
tokenizer = Tokenizer(scanner=Scanner(string))
while True:
    token = tokenizer.nextToken()
    if (token):
        print(token.tokenClass, token.data)
    else:
        break
