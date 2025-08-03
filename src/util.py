import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = {"*": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}

    if delimiter not in delimiters:
        raise ValueError(f"Invalid delimiter: {delimiter}")

    for node in old_nodes:
        if delimiter not in node.text:
            continue
        index = node.text.index(delimiter)
        second_index = node.text.find(delimiter, index + 1)

        new_nodes.extend(
            [
                TextNode(node.text[:index], TextType.TEXT),
                TextNode(node.text[index : second_index + 1], text_type),
                TextNode(node.text[second_index + 1 :], TextType.TEXT),
            ]
        )

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        has_image = re.findall(r"\!\[(.*?)\]\((.*?)\)", node.text)
        if not has_image:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            continue

        split_image_text = node.text.split(")")
        for text in split_image_text:
            if len(text) == 0:
                continue

            matches = re.findall(r"(.*?)\!\[(.*?)\]\((.*)", text)
            if not matches:
                new_nodes.append(TextNode(text, TextType.TEXT))
                continue

            for match in matches:
                if len(match[0]) > 0:
                    new_nodes.append(TextNode(match[0], TextType.TEXT))
                new_nodes.append(TextNode(match[1], TextType.IMAGE, match[2]))

    return new_nodes
