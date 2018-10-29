#!/usr/bin/env python

from StringIO import StringIO


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
