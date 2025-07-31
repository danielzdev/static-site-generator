import unittest

from src.htmlnode import LeafNode


class TestLeafToHTML(unittest.TestCase):
    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "test"})
        self.assertEqual(node.to_html(), '<p class="test">Hello, world!</p>')

    def test_leaf_with_mult_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "test", "id": "test-id"})
        self.assertEqual(node.to_html(), '<p class="test" id="test-id">Hello, world!</p>')

    def test_not_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), '<h1 id="header-1" class="header">Header 1</h1>')

    def test_not_with_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "test", "id": "header-1"})
        self.assertNotEqual(node.to_html(), '<h1 id="header-1" class="test">Header 1</h1>')
