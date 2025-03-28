import functools

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        if self.children is not None:
            children = [child.tag for child in self.children]
        else:
            children = None
        return f'HTMLNode({self.tag}, {self.value}, children: {children}, {self.props})'

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        '''Returns the attributes as a string with a leading whitespace'''
        attributes = ""
        if self.props is not None:
            for key, value in self.props.items():
                attributes += f' {key}="{value}"'

        return attributes


class LeafNode(HTMLNode):
    def __init__(self, tag:  str, value: str, props: dict = None):
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