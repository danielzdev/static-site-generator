import unittest

from src.util import extract_markdown_images, extract_markdown_links


class TestMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://example.com)")
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and another [link](https://example.org)"
        )
        self.assertListEqual([("link", "https://example.com"), ("link", "https://example.org")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )
