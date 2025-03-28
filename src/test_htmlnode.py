import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_values1(self):
        node = HTMLNode("a", "This is a link.", None, {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a link.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'target': '_blank', 'href': 'https://www.boot.dev'})

    def test_values2(self):
        node = HTMLNode(value="plain text")

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "plain text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        attributes = {
            "target": "_blank",
            "href": "https://www.boot.dev"
        }
        node = HTMLNode("a", "This is a link.", None, attributes)

        return self.assertEqual(repr(node),"HTMLNode(a, This is a link., children: None, {'target': '_blank', 'href': 'https://www.boot.dev'})")

    def test_repr_child(self):
        node = HTMLNode("p", "This is a paragraph.", None, None)
        div = HTMLNode("div", None, [node], None)

        return self.assertEqual(repr(div),"HTMLNode(div, None, children: ['p'], None)")

    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph.", None, None)
        return self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link.", None, {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(node.props_to_html(), ' target="_blank" href="https://www.boot.dev"')

if __name__ == "__main__":
    unittest.main()