import unittest

from textnode import TextNode, TextType
from textconverter import (markdown_to_blocks,
                           extract_markdown_images,
                           extract_markdown_links,
                           split_nodes_image,
                           split_nodes_link,
                           split_nodes_delimiter,
                           text_to_textnodes,
                           text_node_to_html_node,
                           )

class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code block node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.abc.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.abc.com"})

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "./cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "./cat.png", "alt": "This is a image node"})

    def test_split_nodes_delimiter_bold(self):
        text_node = TextNode("This text contains **bold** text", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This text contains ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)]

        self.assertListEqual(nodes, expected_result)

    def test_split_nodes_delimiter_bold_double(self):
        text_node = TextNode("This **text** contains **bold** text", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" contains ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)]

        self.assertListEqual(nodes, expected_result)

    def test_split_nodes_delimiter_italic(self):
        text_node = TextNode("This text contains _italic_ text", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        expected_result = [
            TextNode("This text contains ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN)]

        self.assertListEqual(nodes, expected_result)

    def test_split_nodes_delimiter_multiple(self):
        text_node = TextNode("This text contains **bold** and _italic_ text", TextType.PLAIN)
        nodes1 = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        nodes2 = split_nodes_delimiter(nodes1, "_", TextType.ITALIC)
        expected_result = [
            TextNode("This text contains ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN)]

        self.assertListEqual(nodes2, expected_result)

    def test_split_nodes_delimiter_end_of_str(self):
        text_node = TextNode("This text is **bold**", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This text is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD)]

        self.assertListEqual(nodes, expected_result)

    def test_split_nodes_delimiter_no_plain(self):
        text_node = TextNode("`inline code`", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        expected_result = [
            TextNode("inline code", TextType.CODE)]

        self.assertListEqual(nodes, expected_result)

    def test_split_nodes_delimiter_unmatched(self):
        text_node = TextNode("This **text** contains invalid **syntax", TextType.PLAIN)

        with self.assertRaises(ValueError):
            nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image(split_nodes_link([node]))

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.PLAIN,
            ),
            TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.PLAIN,
            ),
        ]

        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = """
This is **text** with an _italic_ word and a `code block` and an \
![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
"""

        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(nodes, expected_result)

    def test_text_to_textnodes_alternative_markdown(self):
        text = "This is __text__ with an *italic* word and a `code block`"

        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
        ]

        self.assertListEqual(nodes, expected_result)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)

        self.assertListEqual(nodes, [])

    def test_text_to_textnodes_no_gap(self):
        text = "This is a **test**_case_"

        nodes = text_to_textnodes(text)
        expected_result = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("test", TextType.BOLD),
            TextNode("case", TextType.ITALIC),
        ]

        self.assertListEqual(nodes, expected_result)

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