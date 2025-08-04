import unittest

from src.markdown_utilities import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single paragraph with no empty lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no empty lines."])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_multiple_empty_lines(self):
        md = """First paragraph


Second paragraph after multiple empty lines"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph after multiple empty lines"])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = """   Leading whitespace paragraph

   Another paragraph with spaces   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Leading whitespace paragraph", "Another paragraph with spaces"])

    def test_markdown_to_blocks_code_block(self):
        md = """Here's some text

```python
def hello():
    print("Hello World")
```

More text after code"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Here's some text", '```python\ndef hello():\n    print("Hello World")\n```', "More text after code"],
        )

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Title

This is a paragraph with **bold** and *italic* text.

1. Numbered list item
2. Another item

> This is a blockquote
> spanning multiple lines

Final paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "This is a paragraph with **bold** and *italic* text.",
                "1. Numbered list item\n2. Another item",
                "> This is a blockquote\n> spanning multiple lines",
                "Final paragraph.",
            ],
        )

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["", ""])
