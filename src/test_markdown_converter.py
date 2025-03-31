import unittest

from markdown_converter import (
    BlockType,
    markdown_to_blocks,
    get_markdown_block_type,
    extract_markdown_links,
    extract_markdown_images,
)

class TestMarkdownConverter(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an image ![cat](https://imgur.com/a/7IPJmIk) and one more ![dog](https://imgur.com/a/OgiTolD)"
        )
        self.assertListEqual([("cat", "https://imgur.com/a/7IPJmIk"),
                              ("dog", "https://imgur.com/a/OgiTolD")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is links to a [cat](https://imgur.com/a/7IPJmIk) and a [dog](https://imgur.com/a/OgiTolD)"
        )
        self.assertListEqual([("cat", "https://imgur.com/a/7IPJmIk"),
                              ("dog", "https://imgur.com/a/OgiTolD")], matches)

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



if __name__ == "__main__":
    unittest.main()