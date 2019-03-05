#!/usr/bin/env python

__author__ = "David Farmer"

import re


def trans_env(separator, txt):
    env = txt.group(1)
    env_inside = txt.group(2)
    end_env = txt.group(3)

    # the main thing to do is change newline + space in env_inside
    # into separator
    env_inside = re.sub("\n\s+", separator, env_inside)

    the_answer = env + "(" + separator + ")"
    the_answer += env_inside + separator + "end"
    the_answer += end_env
    return the_answer


def transform_environment(text, separator=";;"):
    environments = "cases|multiline|system"

    # we will use a regular expression to extract the environment

    # start with 'environemnt:'
    find_environment = r"(" + environments + ")" + ":"
    # throw away white space after ":"
    find_environment += r"\s*"
    # then anything
    find_environment += r"(.*?)"
    # until you reach the end, or a blank line, or an unindented line
    find_environment += "(\n\n|\n\S|$)"

    # the matching pieces will be handed to the trans_env function
    the_answer = re.sub(find_environment,
                        lambda match: trans_env(separator, match),
                        text, 0, re.DOTALL)

    return the_answer
