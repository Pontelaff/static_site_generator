import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_ne(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.test.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("test", TextType.NORMAL, "www.abc.com")
        self.assertEqual(repr(node), "TextNode(test, normal, www.abc.com)")

if __name__ == "__main__":
    unittest.main()