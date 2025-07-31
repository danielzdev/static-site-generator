import unittest

from src.htmlnode import HTMLNode


class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop(self):
        node = HTMLNode(props={"href": 'href="/url"'})
        self.assertEqual(node.props_to_html(), ' href="/url"')

    def test_multiple_props(self):
        node = HTMLNode(
            props={
                "href": 'href="/url"',
                "target": 'target="_blank"',
                "class": 'class="btn"',
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="/url" target="_blank" class="btn"'
        )

    def test_empty_props_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_with_children(self):
        node = HTMLNode(
            children=[HTMLNode()],
            props={"id": 'id="main"', "style": 'style="color:red;"'},
        )
        self.assertEqual(node.props_to_html(), ' id="main" style="color:red;"')


if __name__ == "__main__":
    unittest.main()
