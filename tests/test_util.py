# -*- coding: utf-8 -*-
"""Util Module for Carson Living tests."""

import unittest

# 2.7 support fallback
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from carson_living.util import _response_body_snippet


class TestResponseBodySnippet(unittest.TestCase):
    """_response_body_snippet test class."""

    def test_empty_body_returns_placeholder(self):
        """Test an empty or whitespace-only body returns a placeholder"""
        self.assertEqual('<empty>',
                         _response_body_snippet(Mock(text='')))
        self.assertEqual('<empty>',
                         _response_body_snippet(Mock(text='   \n  ')))
        self.assertEqual('<empty>',
                         _response_body_snippet(Mock(text=None)))

    def test_whitespace_is_collapsed_to_single_line(self):
        """Test multi-line/whitespace-heavy bodies collapse to one line"""
        response = Mock(text='<html>\n  <body>\n    oops\n  </body>\n</html>')
        self.assertEqual('<html> <body> oops </body> </html>',
                         _response_body_snippet(response))

    def test_long_body_is_truncated(self):
        """Test a body longer than the limit is truncated with an ellipsis"""
        response = Mock(text='x' * 500)
        snippet = _response_body_snippet(response, limit=200)
        self.assertEqual(203, len(snippet))
        self.assertTrue(snippet.endswith('...'))
        self.assertEqual('x' * 200 + '...', snippet)

    def test_short_body_is_unmodified(self):
        """Test a body shorter than the limit is returned as-is"""
        response = Mock(text='short body')
        self.assertEqual('short body', _response_body_snippet(response))
