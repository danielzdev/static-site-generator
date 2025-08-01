import unittest

from src.htmlnode import LeafNode, ParentNode


class TestParentNodeToHtml(unittest.TestCase):
    def test_one_child_no_props(self):
        node = ParentNode("p", [LeafNode("div", "This is a div")])
        self.assertEqual(node.to_html(), "<p><div>This is a div</div></p>")

    def test_one_child_with_props(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph", props={"class": "test", "id": "1"})])
        self.assertEqual(node.to_html(), '<div><p class="test" id="1">This is a paragraph</p></div>')

    def test_one_child_with_parent_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "This is a paragraph", props={"class": "test", "id": "1"})],
            props={"class": "parent", "id": "parent1"},
        )
        self.assertEqual(
            node.to_html(), '<div class="parent" id="parent1"><p class="test" id="1">This is a paragraph</p></div>'
        )

    def test_mult_children_no_props(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph"), LeafNode("p", "This is another paragraph")])
        self.assertEqual(node.to_html(), "<div><p>This is a paragraph</p><p>This is another paragraph</p></div>")

    def test_to_html_with_complex_grandchildren(self):
        grandchild1 = LeafNode("b", "bold", props={"class": "bold-text"})
        grandchild2 = LeafNode("i", "italic", props={"id": "i1"})
        grandchild3 = LeafNode("u", "underline", props={"style": "text-decoration:underline;"})

        child1 = ParentNode("span", [grandchild1, grandchild2, grandchild3], props={"data-role": "wrapper"})
        child2 = LeafNode("p", "just a paragraph", props={"class": "plain"})
        child3 = ParentNode("section", [LeafNode("em", "nested")])

        parent_node = ParentNode("div", [child1, child2, child3], props={"id": "main"})

        self.assertEqual(
            parent_node.to_html(),
            '<div id="main">'
            '<span data-role="wrapper"><b class="bold-text">bold</b><i id="i1">italic</i><u style="text-decoration:underline;">underline</u></span>'
            '<p class="plain">just a paragraph</p>'
            "<section><em>nested</em></section>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
