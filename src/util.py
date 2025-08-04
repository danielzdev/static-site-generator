import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}

    if delimiter not in delimiters:
        raise ValueError(f"Invalid delimiter: {delimiter}")

    for node in old_nodes:
        text = node.text
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        offset = len(delimiter)
        while True:
            start = text.find(delimiter)
            if start == -1:
                if text:  # Only add non-empty text nodes
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break

            closing = text.find(delimiter, start + offset)
            if closing == -1:
                if text:  # Only add non-empty text nodes
                    new_nodes.append(TextNode(text, TextType.TEXT))
                break

            if start > 0:
                new_nodes.append(TextNode(text[:start], TextType.TEXT))

            new_nodes.append(TextNode(text[start + offset : closing], text_type))
            text = text[closing + offset :]

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        split_text = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        for text in split_text:
            match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
            if not match and len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            elif match:
                new_nodes.append(TextNode(match[0][0], TextType.IMAGE, match[0][1]))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        split_text = re.split(r"(?<!\!)(\[.*?\]\(.*?\))", node.text)
        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        for text in split_text:
            match = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
            if not match and len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            elif match:
                new_nodes.append(TextNode(match[0][0], TextType.LINK, match[0][1]))

    return new_nodes


def text_to_textnodes(text):
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    split_nodes = [TextNode(text, TextType.TEXT)]

    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)
    for delimiter, text_type in delimiters.items():
        split_nodes = split_nodes_delimiter(split_nodes, delimiter, text_type)

    return split_nodes
