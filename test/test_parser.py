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

    def testDeeVar(self):
        self.compare('d theta', 'd\\theta')
        self.compare('dy/dx', '\\frac{dy}{dx}')
        self.compare('dy/d theta', '\\frac{dy}{d\\theta}')

    def testLiterals(self):
        # numbers
        self.compare('-73', '-73')

        # strings
        self.compare('xyz', 'x y z')
        self.compare('because', '\\text{because }')

        # Greek letters
        self.compare('delta', '\\delta')
        self.compare('Delta', '\\Delta')

    def testEmptyMatrix(self):
        # an empty column
        input = '[[], []]'
        expected = dedent('''
            \\begin{bmatrix}
            \t\\\\
            \t\\\\
            \\end{bmatrix}
        ''').strip()
        self.compare(input, expected)

        # empty row
        input = '[[,]]'
        expected = dedent('''
            \\begin{bmatrix}
            \t & \\\\
            \\end{bmatrix}
        ''').strip()
        self.compare(input, expected)

    def testMatrix(self):
        input = '[[1,2,3], [x/y, sin x]]'
        expected = dedent('''
            \\begin{bmatrix}
            \t1 & 2 & 3\\\\
            \t\\frac{x}{y} & \\sin\,x\\\\
            \\end{bmatrix}
        ''').strip()
        self.compare(input, expected)

        # not a matrix/vector
        self.compare('[]', '[]')

    def testNestedMatrix(self):
        input = '[[ 1, [[ 2, 3], [4, 5]] ]]'
        expected = dedent('''
            \\begin{bmatrix}
            \t1 & \\begin{bmatrix}
            \t2 & 3\\\\
            \t4 & 5\\\\
            \\end{bmatrix}\\\\
            \\end{bmatrix}
        ''').strip()
        self.compare(input, expected)

    def testEmptyMultilineCommands(self):
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
        input = 'x = cases(;;) 1 if x = 0;; 0 otherwise;; end'
        expected = dedent('''
            x = \\begin{cases}
            \t1 && \\text{if } x = 0\\\\
            \t0 && \\text{otherwise }
            \\end{cases}
        ''').strip()
        self.compare(input, expected)

        # input with line breaks
        input = dedent('''
            x = cases:
                1 if x = 0
                0 otherwise
        ''').strip()
        expected = dedent('''
            x = \\begin{cases}
            \t1 && \\text{if } x = 0\\\\
            \t0 && \\text{otherwise }
            \\end{cases}
        ''').strip()
        self.compare(input, expected)

        # system (keyword) of equations
        input = 'system(;;) x + y = 2;; x - y = 3;;end'
        expected = dedent('''
            \\begin{cases}
            \tx + y & = 2\\\\
            \tx - y & = 3
            \\end{cases}
        ''').strip()
        self.compare(input, expected)


if __name__ == '__main__':
    unittest.main()
