import unittest

from markdown_converter import (
    BlockType,
    markdown_to_blocks,
    get_markdown_block_type,
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


if __name__ == "__main__":
    unittest.main()