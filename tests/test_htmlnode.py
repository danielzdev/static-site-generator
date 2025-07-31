import unittest

from src.htmlnode import HTMLNode


class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop(self):
        node = HTMLNode("p", "This is an htmlnode", props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_multiple_props(self):
        node = HTMLNode(
            props={
                "href": "www.google.com",
                "target": "_blank",
                "class": "btn",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="www.google.com" target="_blank" class="btn"'
        )

    def test_empty_props_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_with_children(self):
        node = HTMLNode(
            children=[HTMLNode()],
            props={"id": "main", "style": "color: red;"},
        )
        self.assertEqual(node.props_to_html(), ' id="main" style="color: red;"')


if __name__ == "__main__":
    unittest.main()
