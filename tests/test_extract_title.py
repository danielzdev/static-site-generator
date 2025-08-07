import unittest

from src.markdown_utilities import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        md = "# title"
        self.assertEqual(extract_title(md), "title")

    def test_no_title(self):
        md = "no title"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_title_after_text(self):
        md = """
This is some text
This is meant to go here

# title
"""
        self.assertEqual(extract_title(md), "title")

    def test_middle_of_line_pound(self):
        md = "This is a title I # swear"
        with self.assertRaises(ValueError):
            extract_title(md)
