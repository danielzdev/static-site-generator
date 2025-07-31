import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hi", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Click here", TextType.URL, "https://example.com")
        node2 = TextNode("Click here", TextType.URL, "https://example.com")
        self.assertEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Click here", TextType.URL, "https://example.com")
        node2 = TextNode("Click here", TextType.URL, "https://other.com")
        self.assertNotEqual(node1, node2)

    def test_repr_output(self):
        node = TextNode("Image", TextType.IMAGE, "https://img.com/cat.png")
        expected = "TextNode(text='Image', text_type=TextType.IMAGE, url=https://img.com/cat.png)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
