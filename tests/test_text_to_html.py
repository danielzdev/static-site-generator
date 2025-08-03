import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node


class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_url(self):
        node = TextNode("This is a URL", TextType.LINK, "http://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a URL")
        self.assertEqual(html_node.props["href"], "http://www.example.com")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://www.example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "http://www.example.com/image.jpg")
        self.assertEqual(html_node.props["alt"], "This is an image")
