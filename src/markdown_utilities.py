def markdown_to_blocks(markdown):
    blocks = []
    split_text = markdown.split("\n\n")
    for text in split_text:
        text = text.strip()
        blocks.append(text)

    return blocks
