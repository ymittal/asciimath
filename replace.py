#!/usr/bin/env python

import argparse
import logging
import os.path
import re

from parser.parser import convertToLaTeX

ASCIIMATH_MARKUP_REGEX = r'<m>`(?P<l_ws>\s*)(?P<markup>.*?)(?P<t_ws>\s*)</m>'


def preprocessOneByOne(doc):
    """Replaces AsciiMath tags with those of LaTeX, one by one
    :param doc (str): document str
    :return (str): document str with LaTeX tags
    """

    def repl(match):
        lWs = match.group('l_ws')
        latexMarkup = convertToLaTeX(match.group('markup'))
        tWs = match.group('t_ws')
        return '<m>{}{}{}</m>'.format(lWs, latexMarkup, tWs)

    pattern = re.compile(ASCIIMATH_MARKUP_REGEX, re.DOTALL)
    return re.sub(pattern, repl=repl, string=doc)


def parseArgs():
    def doesFileExist(path):
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(
                '{} does not exist'.format(path))
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xml',
                        help="path to XML file",
                        required=True,
                        type=doesFileExist)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArgs()
    xml_path = args.xml
    with open(xml_path) as xml_file:
        logging.info('Converting AsciiMath to LaTeX...')
        # TODO: read XML file in chunks
        doc = xml_file.read()
        doc = preprocessOneByOne(doc)

    with open(xml_path, 'w') as output_file:
        output_file.write(doc)
        logging.info('Preprocessed XML saved to {}'
                     .format(xml_path))
