# This file is a modified version of analysis.py from Scancode, based on work
# of nexB Inc. and others. See original file at
# https://github.com/nexB/scancode-toolkit/blob/aba31126dcb3ab57f2b885090f7145f69b67351a/src/textcode/analysis.py
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# 
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import unicodedata
import chardet

from gemlock_parser import strings

"""
Utilities to analyze text. Files are the input.
Once a file is read its output are unicode text lines.
All internal processing assumes unicode in and out.
"""


def remove_null_bytes(s):
    """
    Return a string replacing by a space all null bytes.
    There are some rare cases where we can have binary strings that are not
    caught early when detecting a file type, but only late at the line level.
    This help catch most of these cases.
    """
    return s.replace('\x00', ' ')


def as_unicode(line):
    """
    Return a unicode text line from a text line.
    Try to decode line as Unicode. Try first some default encodings,
    then attempt Unicode trans-literation and finally
    fall-back to ASCII strings extraction.
    TODO: Add file/magic detection, unicodedmanit/BS3/4
    """
    if isinstance(line, str):
        return remove_null_bytes(line)

    try:
        s = line.decode('UTF-8')
    except UnicodeDecodeError:
        try:
            # FIXME: latin-1 may never fail
            s = line.decode('LATIN-1')
        except UnicodeDecodeError:
            try:
                # Convert some byte string to ASCII characters as Unicode including
                # replacing accented characters with their non- accented NFKD
                # equivalent. Non ISO-Latin and non ASCII characters are stripped
                # from the output. Does not preserve the original length offsets.
                # For Unicode NFKD equivalence, see:
                # http://en.wikipedia.org/wiki/Unicode_equivalence
                s = unicodedata.normalize('NFKD', line).encode('ASCII')
            except UnicodeDecodeError:
                try:
                    enc = chardet.detect(line)['encoding']
                    s = str(line, enc)
                except UnicodeDecodeError:
                    # fall-back to strings extraction if all else fails
                    s = strings.string_from_string(s)
    return remove_null_bytes(s)


def remove_verbatim_cr_lf_tab_chars(s):
    """
    Return a string replacing by a space any verbatim but escaped line endings
    and tabs (such as a literal \n or \r \t).
    """
    if not s:
        return s
    return s.replace('\\r', ' ').replace('\\n', ' ').replace('\\t', ' ')


def unicode_text_lines(location):
    """
    Return an iterable over unicode text lines from a file at `location` if it
    contains text. Open the file as binary with universal new lines then try to
    decode each line as Unicode.
    """
    with open(location, 'rb') as f:
        for line in f.read().splitlines(True):
            yield remove_verbatim_cr_lf_tab_chars(as_unicode(line))

