#!/usr/bin/env python3
"""Run the whole ARC-2 test suite. Exits non-zero if anything fails.

    python3 run_tests.py
    python3 run_tests.py -v
"""
import sys
import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests", top_level_dir=".")
    verbosity = 2 if "-v" in sys.argv else 1
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
