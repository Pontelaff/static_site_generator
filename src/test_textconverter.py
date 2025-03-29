import unittest

from textnode import TextNode, TextType
from textconverter import text_node_to_html_node, split_nodes_delimiter

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

        self.assertEqual(nodes, expected_result)

    def test_split_nodes_delimiter_italic(self):
        text_node = TextNode("This text contains _italic_ text", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        expected_result = [
            TextNode("This text contains ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN)]

        self.assertEqual(nodes, expected_result)

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

        self.assertEqual(nodes2, expected_result)

    def test_split_nodes_delimiter_end_of_str(self):
        text_node = TextNode("This text is **bold**", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This text is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD)]

        self.assertEqual(nodes, expected_result)

    def test_split_nodes_delimiter_no_plain(self):
        text_node = TextNode("`inline code`", TextType.PLAIN)
        nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        expected_result = [
            TextNode("inline code", TextType.CODE)]

        self.assertEqual(nodes, expected_result)

if __name__ == "__main__":
    unittest.main()