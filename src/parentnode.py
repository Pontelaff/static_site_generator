import functools
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag vor parent node")
        if self.children is None or len(self.children) == 0:
            raise ValueError("missing child nodes for parent node")

        tag_open = f'<{self.tag}{self.props_to_html()}>'
        tag_close = f'</{self.tag}>'
        child_html = functools.reduce(lambda aggregator, child: aggregator + child.to_html(), self.children, "")

        return tag_open + child_html + tag_close