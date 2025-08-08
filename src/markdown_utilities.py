import os

from src.htmlnode import ParentNode
from src.markdown_block import BlockType, get_block_type
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.util import text_to_textnodes


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def convert_block_to_node(block):
    type = get_block_type(block)

    if type == BlockType.CODE:
        return convert_code_block_to_node(block)
    elif type == BlockType.PARAGRAPH:
        return convert_paragraph_block_to_node(block)
    elif type == BlockType.HEADING:
        return convert_heading_block_to_node(block)
    elif type == BlockType.QUOTE:
        return convert_quote_block_to_node(block)
    elif type == BlockType.ORDERED_LIST:
        return convert_ol_list_block_to_node(block)
    elif type == BlockType.UNORDERED_LIST:
        return convert_ul_list_block_to_node(block)
    else:
        pass


def convert_paragraph_block_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def convert_heading_block_to_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def convert_ol_list_block_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def convert_ul_list_block_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def convert_quote_block_to_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def convert_code_block_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    parent_div = ParentNode("div", children=[])
    children = parent_div.children

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = convert_block_to_node(block)
        children.append(node)

    return parent_div


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        line = line.strip()
        if len(line) < 1 or not line.startswith("#"):
            continue
        elif line.startswith("#"):
            line = line.replace("#", "").strip()
            return line
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_node)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in items:
        current_path = os.path.join(dir_path_content, item)

        if os.path.isfile(current_path):
            item = item.replace("md", "html")
            generate_page(current_path, template_path, os.path.join(dest_dir_path, item))
        else:
            copy_path = os.path.join(dest_dir_path, item)
            os.mkdir(copy_path)
            generate_pages_recursive(current_path, template_path, copy_path)
