from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code_block"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, type: TextType, url: str = None):
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, other: "TextNode"):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
