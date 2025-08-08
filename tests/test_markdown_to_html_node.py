import unittest

from src.markdown_utilities import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_one_sentence(self):
        md = "This is a sentence."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a sentence.</p></div>")

    def test_one_setence_with_some_markdown(self):
        md = "This is a sentence with **bold** and _italic_ text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a sentence with <b>bold</b> and <i>italic</i> text.</p></div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        pass

    def test_quote_block(self):
        md = """
>This is a quote block
>This is **another** quote block
>This is a third quote block with an _italic_ word
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block This is <b>another</b> quote block This is a third quote block with an <i>italic</i> word</blockquote></div>",
        )

    def test_multiple_blocks(self):
        md = """
>This is a quote block
>This is **another** quote block
>This is a third quote block with an _italic_ word

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block This is <b>another</b> quote block This is a third quote block with an <i>italic</i> word</blockquote><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
