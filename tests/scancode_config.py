# This file is a modified version of scancode_config.py from Scancode, based on work
# of nexB Inc. and others. See original file at
# https://github.com/nexB/scancode-toolkit/blob/aba31126dcb3ab57f2b885090f7145f69b67351a/src/scancode_config.py
#
# 
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#
import os

# Used for tests to regenerate fixtures with regen=True
REGEN_TEST_FIXTURES = os.getenv('SCANCODE_REGEN_TEST_FIXTURES', False)

