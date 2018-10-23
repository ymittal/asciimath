#!/usr/bin/env python

import re
import os.path
import requests
import logging
import argparse

ASCIIMATH_MARKUP_REGEX = r'<m>`(?P<l_ws>\s*)(?P<markup>.*?)(?P<t_ws>\s*)</m>'

BASE_URL = 'http://localhost:8080'


def convertASCIIMathToLatex(markups):
    """Converts AsciiMath markups to LaTeX
    :param markups (str, list): AsciiMath markup(s)
    :return (str, list): LaTeX str when a single markup
        passed as param, otherwise a list of LaTeX markups
    """
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
    """Deprecated. Replaces AsciiMath markup tags with those of
    LaTeX, all using a single API call.
    :param doc (str): document str
    :return (str): document str with LaTeX tags
    """
    logging.warning('DEPRACATED -- use preprocessBatchV2()')
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
    """Replaces AsciiMath markup tags with those of LaTeX,
    all using a single API call. Use this to minimize network
    traffic if :param doc contains lots of AsciiMath tags.
    :param doc (str): document str
    :return (str): document str with LaTeX tags
    """
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
    """Replaces AsciiMath tags with those of LaTeX, one by one
    :param doc (str): document str
    :return (str): document str with LaTeX tags
    """
    def repl(match):
        lWs = match.group('l_ws')
        latexMarkup = convertASCIIMathToLatex(match.group('markup'))
        tWs = match.group('t_ws')
        return '<m>{}{}{}</m>'.format(lWs, latexMarkup, tWs)

    pattern = re.compile(ASCIIMATH_MARKUP_REGEX, re.DOTALL)
    return re.sub(pattern, repl=repl, string=doc)


def parse_args():
    def does_file_exist(path):
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(
                '{} does not exist'.format(path))
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xml',
                        help="path to XML file",
                        required=True,
                        type=does_file_exist)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    xml_path = args.xml
    with open(xml_path) as xml_file:
        logging.info('Converting AsciiMath to LaTeX...')
        # TODO: read XML file in chunks
        doc = xml_file.read()
        doc = preprocessBatchV2(doc)

    with open(xml_path, 'w') as output_file:
        output_file.write(doc)
        logging.info('Preprocessed XML saved to {}'
                     .format(xml_path))
