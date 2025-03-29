import unittest

from textnode import TextNode, TextType
from textconverter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()