#!/usr/bin/env bash

# sample usage:
# ./pretext.sh -o <output_dir> <stylesheet> <xml>

BASH_DIR=$(dirname "$0")

STYLESHEET=${@:$#-1:1}
XML_FILE=${@:$#}
OTHER_ARGS=${@:1:$#-2}

python $BASH_DIR/replace.py --xml $XML_FILE
xsltproc $OTHER_ARGS $STYLESHEET $XML_FILE
