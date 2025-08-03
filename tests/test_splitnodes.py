import unittest

from src.textnode import TextNode, TextType
from src.util import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_valid_split_code(self):
        nodes = [TextNode("Here is `code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result[0].text, "Here is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_no_delimiter_present(self):
        nodes = [TextNode("No formatting here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [TextNode("No formatting here", TextType.TEXT)])

    def test_invalid_delimiter(self):
        nodes = [TextNode("Some text with `code`", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "~", TextType.CODE)

    def test_multiple_textnodes_mixed_delimiters(self):
        nodes = [
            TextNode("No delimiter here", TextType.TEXT),
            TextNode("Middle has *bold* text, neat.", TextType.TEXT),
            TextNode("Another one with no match", TextType.TEXT),
            TextNode("Some *MORE* bold text :D", TextType.TEXT),
            TextNode("Middle has _italic_ text, neat.", TextType.ITALIC),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)

        self.assertEqual(len(result), 9)

        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "Middle has ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, " text, neat.")
        self.assertEqual(result[3].text_type, TextType.TEXT)

        self.assertEqual(result[4].text, "Another one with no match")
        self.assertEqual(result[4].text_type, TextType.TEXT)

        self.assertEqual(result[5].text, "Some ")
        self.assertEqual(result[5].text_type, TextType.TEXT)
        self.assertEqual(result[6].text, "MORE")
        self.assertEqual(result[6].text_type, TextType.BOLD)
        self.assertEqual(result[7].text, " bold text :D")
        self.assertEqual(result[7].text_type, TextType.TEXT)

        self.assertEqual(result[8].text, "Middle has _italic_ text, neat.")
        self.assertEqual(result[8].text_type, TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
