import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_values(self):
        node = LeafNode("a", "This is a link.", {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a link.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'target': '_blank', 'href': 'https://www.boot.dev'})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "BOLD")
        self.assertEqual(node.to_html(), "<b>BOLD</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link.", {'target': '_blank', 'href': 'https://www.boot.dev'})
        self.assertEqual(node.to_html(), '<a target="_blank" href="https://www.boot.dev">This is a link.</a>')

    def test_lead_to_html_raw(self):
        node = LeafNode(None, "plain text")

        self.assertEqual(node.to_html(), 'plain text')

    def test_leaf_to_html_exept(self):
        node = LeafNode("p", None)

        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()