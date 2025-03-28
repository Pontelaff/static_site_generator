import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    ##################################
    # HTMLNode
    ##################################
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

        self.assertEqual(repr(node),"HTMLNode(a, This is a link., children: None, {'target': '_blank', 'href': 'https://www.boot.dev'})")

    def test_repr_child(self):
        node = HTMLNode("p", "This is a paragraph.", None, None)
        div = HTMLNode("div", None, [node], None)

        self.assertEqual(repr(div),"HTMLNode(div, None, children: ['p'], None)")

    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph.", None, None)
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link.", None, {'target': '_blank', 'href': 'https://www.boot.dev'})

        self.assertEqual(node.props_to_html(), ' target="_blank" href="https://www.boot.dev"')


    ##################################
    # LeafNode
    ##################################
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


    ##################################
    # ParentNode
    ##################################
    def test_parent_node_values(self):
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