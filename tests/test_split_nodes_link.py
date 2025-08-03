import unittest

from src.textnode import TextNode, TextType
from src.util import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_no_link(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text with no link", TextType.TEXT)],
            new_nodes,
        )

    def test_multiple_nodes_with_multiple_links(self):
        node1 = TextNode(
            "First node with [link1](https://example.com) and [link2](https://google.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Second node [link3](https://github.com) middle text [link4](https://stackoverflow.com) end",
            TextType.TEXT,
        )
        node3 = TextNode(
            "Third node with single [link5](https://reddit.com) link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://google.com"),
                TextNode("Second node ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "https://github.com"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("link4", TextType.LINK, "https://stackoverflow.com"),
                TextNode(" end", TextType.TEXT),
                TextNode("Third node with single ", TextType.TEXT),
                TextNode("link5", TextType.LINK, "https://reddit.com"),
                TextNode(" link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_partial_match(self):
        node = TextNode("First node with only a partial regex match [link](url", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First node with only a partial regex match [link](url", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_only_link(self):
        node = TextNode("[only link](https://only.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only link", TextType.LINK, "https://only.com"),
            ],
            new_nodes,
        )

    def test_link_with_empty_text(self):
        node = TextNode("Text with [](https://empty.com) empty link text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://empty.com"),
                TextNode(" empty link text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_ignore_image(self):
        node = TextNode("This has ![image](img.png) but no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has ![image](img.png) but no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_and_image(self):
        node = TextNode("This has ![image](img.png) and [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has ![image](img.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )
