import unittest

from src.markdown_block import BlockType, get_block_type
from src.markdown_utilities import markdown_to_blocks


class TestGetBlockType(unittest.TestCase):
    def test_get_block_type(self):
        block = "- This is a list\n- with items"
        type = get_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, type)

    def test_ordered_list(self):
        block = "1. This is a list\n2. with items"
        type = get_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, type)

    def test_multiple_blocks(self):
        blocks = [
            "- This is a list\n- with items",
            "1. This is a list\n2. with items",
            "# This is a heading",
            "This is a paragraph",
        ]
        types = [get_block_type(block) for block in blocks]
        self.assertEqual(
            [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST, BlockType.HEADING, BlockType.PARAGRAPH], types
        )

    def test_markdown_doc_with_types(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        types = [get_block_type(block) for block in blocks]
        self.assertEqual([BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.UNORDERED_LIST], types)
