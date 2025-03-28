class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None) -> "HTMLNode":
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
