#!/usr/env/bin python

from src.tokenizer import TokenClass


def _getGreekLettersToLaTeX():
    greekLetters = TokenClass.getGreekLetters()
    res = {}
    for letter in greekLetters:
        name = letter.name
        if name.endswith('_C'):
            name = name[:-2].capitalize()
        else:
            name = name.lower()
        res[letter] = '\\%s' % name

    return res


def _getConstantSymbolsToLaTeX():
    return {
        # operations
        TokenClass.PLUS: '+',
        TokenClass.MINUS: '-',
        TokenClass.CDOT: '\\cdot',
        TokenClass.ASTERIX: '\\ast',
        TokenClass.DIV: '/',
        TokenClass.DIV_KG: '\\div',
        TokenClass.SUMMATION: '\\sum',
        TokenClass.PROD: '\\prod',
        TokenClass.CAP: '\\cap',
        TokenClass.CUP: '\\cup',
        TokenClass.WEDGE: '\\wedge',
        TokenClass.VEE: '\\vee',
        TokenClass.TIMES: '\\times',
        TokenClass.SLASH: '/',
        TokenClass.LIMIT: '\\lim',

        # relational symbols
        TokenClass.EQUALS: '=',
        TokenClass.LT: '\\lt',
        TokenClass.LE: '\\le',
        TokenClass.GT: '\\gt',
        TokenClass.GE: '\\ge',
        TokenClass.NE: '\\ne',
        TokenClass.APPROX: '\\approx',
        TokenClass.IN: '\\in',
        TokenClass.NOTIN: '\\notin',
        TokenClass.SUBSET: '\\subset',
        TokenClass.SUPSET: '\\supset',
        TokenClass.SUBSETEQ: '\\subseteq',
        TokenClass.SUPSETEQ: '\\supseteq',
        TokenClass.CONGRUENCE: '\\cong',
        TokenClass.PROPORTIONAL: '\\propto',
        TokenClass.EQUIV: '\\equiv',
        TokenClass.NOTSUBSET: '\\not\\subset',
        TokenClass.NOTSUPSET: '\\not\\supset',
        TokenClass.NOTSUBSETEQ: '\\subsetneq',
        TokenClass.NOTSUPSETEQ: '\\supsetneq',

        # logical symbols
        TokenClass.IMPLIES: '\\implies',
        TokenClass.IFF: '\\iff',
        TokenClass.NOT: '\\neg',
        TokenClass.FORALL: '\\forall',
        TokenClass.EXISTS: '\\exists',

        # miscellaneous
        TokenClass.SQRT: '\\surd',
        TokenClass.ROOT: '\\surd',
        TokenClass.INTEGRAL: '\\int',
        TokenClass.DEL: '\\partial',
        TokenClass.GRAD: '\\nabla',
        TokenClass.INF: '\\infty',
        TokenClass.ALEPH: '\\aleph',
        TokenClass.SET_C: '\\mathbb{C}',
        TokenClass.SET_N: '\\mathbb{N}',
        TokenClass.SET_Q: '\\mathbb{Q}',
        TokenClass.SET_R: '\\mathbb{R}',
        TokenClass.SET_Z: '\\mathbb{Z}',
        TokenClass.THEREFORE: '\\therefore',
        TokenClass.BECAUSE: '\\because',
        TokenClass.PLUSMINUS: '\\pm',
        TokenClass.OINT: '\\oint',
        TokenClass.FRAC: '/',
        TokenClass.UNDERSCORE: '\\_',
        TokenClass.CARAT: '\\hat{}',

        # arrows and accents
        TokenClass.RARR: '\\rightarrow',
        TokenClass.LARR: '\\leftarrow',
        TokenClass.LRARR: '\\leftrightarrow',
        TokenClass.RARR_THICK: '\\Rightarrow',
        TokenClass.LARR_THICK: '\\Leftarrow',
        TokenClass.LRARR_THICK: '\\Leftrightarrow',
        TokenClass.UARR: '\\uparrow',
        TokenClass.DARR: '\\downarrow',
        TokenClass.MAPSTO: '\\mapsto',

        # standard functions
        TokenClass.SIN: '\\sin',
        TokenClass.COS: '\\cos',
        TokenClass.TAN: '\\tan',
        TokenClass.SEC: '\\sec',
        TokenClass.CSC: '\\csc',
        TokenClass.COT: '\\cot',
        TokenClass.ARCSIN: '\\arcsin',
        TokenClass.ARCCOS: '\\arccos',
        TokenClass.ARCTAN: '\\arctan',
        TokenClass.SINH: '\\sinh',
        TokenClass.COSH: '\\cosh',
        TokenClass.TANH: '\\tanh',
        TokenClass.EXP: '\\exp',
        TokenClass.LOG: '\\log',
        TokenClass.LN: '\\ln',
        TokenClass.DET: '\\det',
        TokenClass.DIM: '\\dim',
        TokenClass.MOD: '\\mod',
        TokenClass.GCD: '\\gcd',
        TokenClass.LCM: '\\text{lcm}',
        TokenClass.MIN: '\\min',
        TokenClass.MAX: '\\max',
        TokenClass.F: 'f',
        TokenClass.G: 'g',
    }


def _getConstantSymbolsWithResizedBrackets():
    return {
        # operations
        TokenClass.SUMMATION,
        TokenClass.PROD,
        TokenClass.LIMIT,

        # miscellaneous
        TokenClass.INTEGRAL,
        TokenClass.OINT
    }
