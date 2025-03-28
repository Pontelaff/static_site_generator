from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("missing value for leaf node")

        if self.tag == None:
            tag_open, tag_close = "", ""
        else:
            tag_open = f'<{self.tag}{self.props_to_html()}>'
            tag_close = f'</{self.tag}>'

        return f"{tag_open}{self.value}{tag_close}"
