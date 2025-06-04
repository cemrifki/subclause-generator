#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module is created to handle preprocessing operations.
@author: Cem Rıfkı Aydın
"""

import re

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')


def normalize_tokenize(string):
    """
    This is a basic, generic tokenizer.

    :param string: Text to be tokenized.
    :type string: str
    :return: String in a tokenized form that is to be split later by other helper methods.
    :rtype: str
    """
    string = string.lower()
    # HTML tags are removed by the below line of code.
    string = tag_re.sub(' ', string)
    # This is added to reduce the same characters appearing consecutively more than twice
    # to the same two chars only.
    string = re.sub(r"(.)(\1)\1{2,}", r"\1\1\1", string)
    # Added, since mentions (e.g. @trump) do not contribute to sentiment.
    string = re.sub(r"@[a-zA-Z0-9()#,!?:=;\-\\'`./]+", r"", string)
    # Some extra chars are added to be taken into account.
    string = re.sub(r"[^A-Za-z0-9()#,!?:=;\-\\'`./]", " ", string)

    # Numeric forms and emoticons, such as 22:30, are not disrupted.
    string = re.sub(r"([^\d)(])([,.:;]+)([^\d()]|$)", r"\1 \2 \3", string)
    # The punctuation marks "?" and "!" can be indicative of expressing sentiment. These
    # are therefore not removed.
    string = re.sub(r"([!?]+)", r" \1 ", string)

    # The below four regex commands are implemented to put blank spaces before or after
    # parens without disrupting emoticons.

    string = re.sub(r"\(([A-Za-z0-9,!?\-\\'`])", r"( \1", string)
    string = re.sub(r"([A-Za-z0-9,!?\-\\'`])\(", r"\1 (", string)

    string = re.sub(r"([A-Za-z0-9,!?\-\\'`])\)", r"\1 )", string)
    string = re.sub(r"\)([A-Za-z0-9,!?\-\\'`])", r") \1", string)

    # "(?!)" and similar forms that likely indicate sarcasm are kept.
    string = re.sub(r"(\() +([?!]+) +(\))", r"\1\2\3", string)
    # Useless parens are removed.
    string = re.sub(r"(^|[ ])+([()]+)([ ]+|$)", r" ", string)
    # Other useless punctuations are also eliminated.
    string = re.sub(r"(^|[ ])+([.;,]+)([ ]+|$)", r" ", string)

    # Emoticons ":s" and ":D".
    string = re.sub(r"((\s|^)[:]+)[ ]+([dDsSpP]+(\s|$))", r"\1\3", string)
    # Emoticon handling.
    string = re.sub(r"([:;.]+)([()dDsSpP]+)", r" \1\2 ", string)

    string = re.sub(r"\s{2,}", " ", string)
    return string
