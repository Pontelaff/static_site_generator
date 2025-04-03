import unittest

from markdown_converter import (
    BlockType,
    markdown_to_html_nodes,
    markdown_to_blocks,
    get_markdown_block_type,
    extract_markdown_heading,
)

class TestMarkdownConverter(unittest.TestCase):
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

    def test_markdown_to_blocks_exessive_newlines(self):
        md = """
This is a paragraph

This is another paragraph


This paragraph is too far down

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is another paragraph",
                "This paragraph is too far down",
            ],
        )

    def test_get_block_type_heading(self):
        h1 = "# This is a h1 heading"
        h2 = "## This is a h2 heading"
        h7 = "####### This heading is too deep"
        faulty_heading = "This is not a # heading"
        empty_heading = "# "
        multi_line = "# This is a heading\nwith body"

        self.assertEqual(get_markdown_block_type(h1), BlockType.HEADING)
        self.assertEqual(get_markdown_block_type(h2), BlockType.HEADING)
        self.assertEqual(get_markdown_block_type(h7), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(faulty_heading), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(empty_heading), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(multi_line), BlockType.PARAGRAPH)

    def test_get_block_type_code(self):
        code_block = """```py
This  is a multiline codeblock
```"""
        single_line = "```This is not a code block```"
        trailing = "```This is not a code```block"
        leading = "Neither```is this```"
        # unmatched = "```This code block ``` is unmatched```"

        self.assertEqual(get_markdown_block_type(code_block), BlockType.CODE)
        self.assertEqual(get_markdown_block_type(single_line), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(trailing), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(leading), BlockType.PARAGRAPH)
        # self.assertEqual(get_markdown_block_type(unmatched), BlockType.PARAGRAPH)

    def test_get_block_type_quote(self):
        quote_single_line = "> Aela iacta est"
        quote_multi_line = """> To be or not to be
> That is the question"""
        quote_incomplete = """> Don't trust anything you read on the internet
- Abraham Lincoln"""

        self.assertEqual(get_markdown_block_type(quote_single_line), BlockType.QUOTE)
        self.assertEqual(get_markdown_block_type(quote_multi_line), BlockType.QUOTE)
        self.assertEqual(get_markdown_block_type(quote_incomplete), BlockType.PARAGRAPH)

    def test_get_block_type_unordered_list(self):
        single_item = "- item"
        multiple_items = """- first
- second
- third"""
        incomplete_list = """- first
- second
third"""

        self.assertEqual(get_markdown_block_type(single_item), BlockType.UNORDERED_LIST)
        self.assertEqual(get_markdown_block_type(multiple_items), BlockType.UNORDERED_LIST)
        self.assertEqual(get_markdown_block_type(incomplete_list), BlockType.PARAGRAPH)

    def test_get_block_type_ordered_list(self):
        single_item = "1. item"
        multiple_items = """1. first
2. second
3. third"""
        incomplete_list = """1. first
2. second
third"""
        wrong_order = """1. first
2. second
2. third"""
        missing_point = """1. first
2. second
3 third"""

        self.assertEqual(get_markdown_block_type(single_item), BlockType.ORDERED_LIST)
        self.assertEqual(get_markdown_block_type(multiple_items), BlockType.ORDERED_LIST)
        self.assertEqual(get_markdown_block_type(incomplete_list), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(wrong_order), BlockType.PARAGRAPH)
        self.assertEqual(get_markdown_block_type(missing_point), BlockType.PARAGRAPH)

    def test_headings(self):
        md ="""
# Heading 1

## Heading 2

"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()

        expected_result = "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>"

        self.assertEqual(html, expected_result)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quotes(self):
        md ="""
> Quote with
> two lines
"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()

        expected_result = "<div><blockquote>Quote with two lines</blockquote></div>"

        self.assertEqual(html, expected_result)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is a **bold item**
2. This item is _italic_
"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a <b>bold item</b></li><li>This item is <i>italic</i></li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a **bold item**
- This item is _italic_
- [link](www.xyz.com)
"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is a <b>bold item</b></li><li>This item is <i>italic</i></li><li><a href="www.xyz.com">link</a></li></ul></div>',
        )

    def test_markdown_to_html(self):
        md ="""
# Heading

Text paragraph
with two **lines**
and a [link](www.xyz.com)

> Quote with
> two _lines_
"""
        node = markdown_to_html_nodes(md)
        html = node.to_html()

        expected_result = '<div><h1>Heading</h1><p>Text paragraph with two <b>lines</b> and a <a href="www.xyz.com">link</a></p><blockquote>Quote with two <i>lines</i></blockquote></div>'

        self.assertEqual(html, expected_result)

    def test_extract_heading(self):
        md ="""
# Heading

This is a paragraph

## And another heading
"""
        self.assertEqual(extract_markdown_heading(md), "Heading")

    def test_extract_heading2(self):
        md ="""
Text before the heading

# Heading

This is a paragraph
"""
        self.assertEqual(extract_markdown_heading(md), "Heading")

    def test_extract_heading_missing(self):
        md ="""
The heading is missing :(

## This is a second level heading
"""
        with self.assertRaises(ValueError):
            extract_markdown_heading(md)



if __name__ == "__main__":
    unittest.main()