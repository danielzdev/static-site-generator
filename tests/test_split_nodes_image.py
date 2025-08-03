import unittest

from src.textnode import TextNode, TextType
from src.util import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_no_image(self):
        node = TextNode("This is text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no image", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with some text at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_nodes_with_multiple_images(self):
        node1 = TextNode(
            "First node with ![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Second node ![image3](https://example.com/img3.png) middle text ![image4](https://example.com/img4.png) end",
            TextType.TEXT,
        )
        node3 = TextNode(
            "Third node with single ![image5](https://example.com/img5.png) image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://example.com/img2.png"),
                TextNode("Second node ", TextType.TEXT),
                TextNode("image3", TextType.IMAGE, "https://example.com/img3.png"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("image4", TextType.IMAGE, "https://example.com/img4.png"),
                TextNode(" end", TextType.TEXT),
                TextNode("Third node with single ", TextType.TEXT),
                TextNode("image5", TextType.IMAGE, "https://example.com/img5.png"),
                TextNode(" image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_partial_match(self):
        node = TextNode("First node with only a partial regex match ![image](url", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First node with only a partial regex match ![image](url", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_single_image_at_start(self):
        node = TextNode("![start image](https://start.com/img.png) with text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://start.com/img.png"),
                TextNode(" with text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_single_image_at_end(self):
        node = TextNode("Text before ![end image](https://end.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://end.com/img.png"),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode("![only image](https://only.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://only.com/img.png"),
            ],
            new_nodes,
        )

    def test_image_with_empty_text(self):
        node = TextNode("Text with ![](https://empty.com/img.png) empty image text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://empty.com/img.png"),
                TextNode(" empty image text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_and_link(self):
        node = TextNode(
            "First node with ![image](https://example.com/img1.png) and [link](https://example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" and [link](https://example.com)", TextType.TEXT),
            ],
            new_nodes,
        )
