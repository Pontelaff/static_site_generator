import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_leaf_node_values(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("div", [child_node], {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [child_node])
        self.assertEqual(node.props, {'target': '_blank', 'href': 'https://www.boot.dev'})

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("b", "first child")
        child_node2 = LeafNode(None, "second child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><b>first child</b>second child</div>")

    def test_to_html_with_attributes(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("a", [child_node], {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(
            parent_node.to_html(),
            '<a target="_blank" href="https://www.boot.dev"><span>child</span></a>'
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)

        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])

        self.assertRaises(ValueError, parent_node.to_html)

if __name__ == "__main__":
    unittest.main()