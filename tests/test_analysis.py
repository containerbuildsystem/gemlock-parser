# This file is a modified version of test_analysis.py from Scancode, based on work
# of nexB Inc. and others. See original file at
# https://github.com/nexB/scancode-toolkit/blob/a15174f31efaf8816e8c9a65c9f85c4beffc0227/tests/textcode/test_analysis.py
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import pytest
import json
import os.path

from commoncode.testcase import FileBasedTesting

from scancode_config import REGEN_TEST_FIXTURES
from gemlock_parser.analysis import unicode_text_lines, as_unicode


def check_text_lines(result, expected_file, regen=REGEN_TEST_FIXTURES):
        if regen:
            with open(expected_file, 'w') as tf:
                json.dump(result, tf, indent=2)
        with open(expected_file, 'rb') as tf:
            expected = json.load(tf)
        assert result == expected


class TestAnalysis(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_unicode_text_lines_handles_weird_xml_encodings(self):
        test_file = self.get_test_loc('analysis/weird_encoding/easyconf-0.9.0.pom')
        result = list(unicode_text_lines(test_file))
        expected_file = self.get_test_loc('analysis/weird_encoding/easyconf-0.9.0.pom.expected')
        check_text_lines(result, expected_file)

    def test_unicode_text_lines_replaces_null_bytes_with_space(self):
        test_file = self.get_test_loc('analysis/text-with-trailing-null-bytes.txt')
        result = list(unicode_text_lines(test_file))
        expected_file = self.get_test_loc('analysis/text-with-trailing-null-bytes.txt.expected')
        check_text_lines(result, expected_file, regen=REGEN_TEST_FIXTURES)

    def test_as_unicode_converts_bytes_to_unicode(self):
        test_line = '    // as defined in https://tools.ietf.org/html/rfc2821#section-4.1.2.'.encode()
        result = as_unicode(test_line)
        assert type(result) == str

    def test_as_unicode_from_bytes_replaces_null_bytes_with_space(self):
        test = b'\x00is designed to give them, \x00BEFORE the\x00\x00\x00\x00\x00\x00'
        result = as_unicode(test)
        expected = ' is designed to give them,  BEFORE the      '
        assert result == expected

    def test_as_unicode_from_unicode_replaces_null_bytes_with_space(self):
        test = '\x00is designed to give them, \x00BEFORE the\x00\x00\x00\x00\x00\x00'
        result = as_unicode(test)
        expected = ' is designed to give them,  BEFORE the      '
        assert result == expected