#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mercury206
----------------------------------

Tests for `mercury206` package.
"""

import unittest
import doctest

import mercury206.protocol
import mercury206.utils


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(mercury206.protocol))
    tests.addTests(doctest.DocTestSuite(mercury206.utils))
    return tests


if __name__ == '__main__':
    unittest.main()