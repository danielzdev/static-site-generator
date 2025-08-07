import os

from src.htmlnode import LeafNode, ParentNode
from src.markdown_block import BlockType, get_block_type
from src.textnode import text_node_to_html_node
from src.util import text_to_textnodes


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]


def markdown_to_html_node(markdown):
    parent_div = ParentNode("div", children=[])
    children = parent_div.children

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = convert_block_to_node(block)
        children.append(node)

    return parent_div


def convert_block_to_node(block):
    type = get_block_type(block)

    if type == BlockType.CODE:
        return convert_code_block_to_node(block)
    elif type == BlockType.PARAGRAPH:
        return convert_paragraph_block_to_node(block)
    elif type == BlockType.HEADING:
        return convert_heading_block_to_node(block)
    else:
        return convert_special_block_to_node(block)


def convert_code_block_to_node(block):
    lines = block.splitlines(keepends=True)
    cleaned = lines[1:-1]
    only_code = "".join(cleaned)
    return ParentNode("pre", children=[LeafNode("code", only_code)])


def convert_paragraph_block_to_node(block):
    block = block.replace("\n", " ")

    leaf_nodes = []
    text_nodes = text_to_textnodes(block)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        leaf_nodes.append(html_node)

    return ParentNode("p", children=leaf_nodes)


def convert_heading_block_to_node(block):
    headings = {1: "h1", 2: "h2", 3: "h3", 4: "h4", 5: "h5", 6: "h6"}

    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break

    tag = headings[count]
    text = block[count + 1 :]
    text_nodes = text_to_textnodes(text)
    leaf_nodes = [text_node_to_html_node(n) for n in text_nodes]
    return ParentNode(tag, leaf_nodes)


def convert_special_block_to_node(block):
    parent_tags = {">": "blockquote", "-": "ul", "1": "ol"}
    tag = parent_tags[block[0]]
    parent = ParentNode(tag, children=[])

    lines = block.splitlines()
    for line in lines:
        line = line[2:] if tag == "ol" else line[1:]
        text_nodes = text_to_textnodes(line.strip())

        leaf_nodes = []
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            leaf_nodes.append(html_node)

        child_tag = "p" if tag == "blockquote" else "li"
        parent_node = ParentNode(child_tag, children=leaf_nodes)
        parent.children.append(parent_node)

    return parent


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
    print(f"Generating page from {from_path} to {dest_path} using {template_path}....")
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
