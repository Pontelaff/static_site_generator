import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_images(markdown: str) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", markdown)

def extract_markdown_links(markdown: str) -> list[tuple]:
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", markdown)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    clean_blocks = [block.strip() for block in blocks if block != ""]

    return clean_blocks

