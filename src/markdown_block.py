from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def get_block_type(block) -> BlockType:
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    split_text = block.split("\n")
    is_unorderd_list = True
    is_qoute_block = True
    is_ordered_list = True

    for index in range(len(split_text)):
        correct_start = str(index + 1) + ". "
        if not split_text[index].startswith(correct_start):
            is_ordered_list = False
        if not split_text[index].startswith(">"):
            is_qoute_block = False
        if not split_text[index].startswith("-"):
            is_unorderd_list = False

    if is_qoute_block:
        return BlockType.QUOTE
    elif is_unorderd_list:
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
