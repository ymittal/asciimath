from collections import deque

from scanner import Scanner
from tokenizer import Tokenizer, TokenClass


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


string = 'a !in B ** CC darr 2 = 2'
tokenizer = Tokenizer(scanner=Scanner(string))
while True:
    token = tokenizer.nextToken()
    if token.tokenClass == TokenClass.EOF:
        break
    elif token and token.data:
        print token.tokenClass, ':', token.data
    elif token:
        print token.tokenClass
