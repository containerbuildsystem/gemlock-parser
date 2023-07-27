# gemlock-parser

This repository contains Gemfile.lock parser vendored from [ScanCode
toolkit](https://github.com/nexB/scancode-toolkit). One of the main goals is to
make sure that RubyGems dependencies are parsed without executing arbitrary Ruby
code.

## Updating

To update the repository based on upstream changes, run `hack/update-from-upstream.sh`.

* for `gemfile_lock.py` and its tests, the script updates everything below the import
  block
* for the supporting files, the script updates the existing top-level definitions
  * functions, classes, constants, module docstrings

Inspect the changes carefully, make adjustments as necessary. Make sure unit tests
are passing.

Port the relevant unit test changes from [`test_analysis.py`][test_analysis.py]
manually, the update script is not smart enough to do that.

[test_analysis.py]: https://github.com/nexB/scancode-toolkit/blob/develop/tests/textcode/test_analysis.py
