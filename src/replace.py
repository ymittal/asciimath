#!/usr/bin/env python

import re
import requests

ASCIIMATH_MARKUP_REGEX = r'<m>`(?P<l_ws>\s*)(?P<markup>.*?)(?P<t_ws>\s*)</m>'

BASE_URL = 'http://localhost:8080'


def convertASCIIMathToLatex(markups):
    if not markups:
        return []

    if not isinstance(markups, (list, )):
        markups = [markups]

    url = '{}/api/translate'.format(BASE_URL)
    r = requests.get(url=url, data={
        'markups': list(markups)
    })
    r = r.json()
    return r if len(r) > 1 else r[0]


def preprocessBatch(doc):
    pattern = re.compile(ASCIIMATH_MARKUP_REGEX, re.DOTALL)
    asciiMarkups = []
    for match in re.finditer(pattern, doc):
        asciiMarkups.append((match.group('markup'), match.span('markup')))

    latexMarkups = convertASCIIMathToLatex([m[0] for m in asciiMarkups])

    res = []
    prevStart = 0
    for idx in range(len(latexMarkups)):
        currSpan = asciiMarkups[idx][1]
        res.extend([
            doc[prevStart:currSpan[0]],
            latexMarkups[idx]
        ])
        prevStart = currSpan[1]
    res.append(doc[prevStart:])

    return ''.join(res)


def preprocessBatchV2(doc):
    pattern = re.compile(ASCIIMATH_MARKUP_REGEX, re.DOTALL)
    asciiMarkups = []
    for match in re.finditer(pattern, doc):
        asciiMarkups.append(match.group('markup'))

    latexMarkups = convertASCIIMathToLatex(asciiMarkups)

    def repl(match):
        lWs = match.group('l_ws')
        latexMarkup = latexMarkups.pop(0)
        tWs = match.group('t_ws')
        return '<m>{}{}{}</m>'.format(lWs, latexMarkup, tWs)

    return re.sub(pattern, repl=repl, string=doc)


def preprocessOneByOne(doc):
    def repl(match):
        lWs = match.group('l_ws')
        latexMarkup = convertASCIIMathToLatex(match.group('markup'))
        tWs = match.group('t_ws')
        return '<m>{}{}{}</m>'.format(lWs, latexMarkup, tWs)

    pattern = re.compile(ASCIIMATH_MARKUP_REGEX, re.DOTALL)
    return re.sub(pattern, repl=repl, string=doc)


from textwrap import dedent
print(preprocessBatchV2(dedent('''
    Hello world
    <m>`1+sqrt(2) </m>
    Haha!
    <m>{\sqrt{55}}</m>
    <m>`

        1/3
    </m>
''')))
