import unittest
from textwrap import dedent

from src.parser import convertToLaTeX


class TestParser(unittest.TestCase):

    def compare(self, input, expected):
        result = convertToLaTeX(input)
        self.assertEquals(result, expected)

    def testUnary(self):
        self.compare('sqrt x', '\\sqrt{x}')
        self.compare('vec x/x', '\\vec{\\frac{x}{x}}')
        self.compare('dot(x)', '\\dot{x}')
        self.compare('ddot x y', '\\ddot{x} y')

    def testBinary(self):
        self.compare('frac x y', '\\frac{x}{y}')
        self.compare('root(x)(y)', '\\sqrt[x]{y}')

    def testInvertibleFunctions(self):
        self.compare('sin x', '\\sin\,x')
        self.compare('cos((x))', '\\cos\,(x)')
        self.compare('tan^-1 x', '\\tan^{-1}x')
        self.compare('exp^{2}x', '\\exp^{2}x')

    def testBrackets(self):
        self.compare('(x){y}', '(x) \\{y\\}')

        # binary
        self.compare('(frac x y)', '\\left(\\frac{x}{y}\\right)')

        # Invertible funcs
        self.compare('(sin^-1 x)', '\\left(\\sin^{-1}x\\right)')
        self.compare('(sin x)', '(\\sin\,x)')

    def testLiterals(self):
        # numbers
        self.compare('-73', '-73')

        # strings
        self.compare('xyz', 'x y z')
        self.compare('because', '\\text{because }')

        # Greek letters
        self.compare('delta', '\\delta')
        self.compare('Delta', '\\Delta')

    def testBlankMultiline(self):
        input = 'multiline(;;)end'
        expected = dedent('''
            \\begin{align}
            \\end{align}
        ''').strip()
        self.compare(input, expected)

        input = 'cases(;;)end'
        expected = dedent('''
                    \\begin{cases}
                    \\end{cases}
                ''').strip()
        self.compare(input, expected)

    def testMultiline(self):
        # single line
        input = 'multiline(;;)x=y because y in RR;;end'
        expected = dedent('''
            \\begin{align}
            \tx & = y && \\text{because } y \\in \\mathbb{R}
            \\end{align}    
        ''').strip()
        self.compare(input, expected)

        # multiple lines
        input = 'multiline(;;)x=y;;>=z;;end'
        expected = dedent('''
            \\begin{align}
            \tx & = y\\\\
            \t& \\ge z
            \\end{align}
        ''').strip()
        self.compare(input, expected)

        # input with line breaks (inconsistent spacing)
        input = dedent('''
            multiline:
              x = y
                  >= z
        ''').strip()
        expected = dedent('''
            \\begin{align}
            \tx & = y\\\\
            \t& \\ge z
            \\end{align}
        ''').strip()
        self.compare(input, expected)

    def testCases(self):
        # system keyword
        pass


if __name__ == '__main__':
    unittest.main()
