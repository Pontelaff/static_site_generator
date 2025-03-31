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

def is_ordered_list(markdown: str) -> bool:
    for i, line in enumerate(markdown.split("\n")):
        num = line.split(".")[0]
        if num != f"{i + 1}":
            return False
    return True

def get_markdown_block_type(markdown: str) -> BlockType:
    # TODO: avoid matching code blocks with an injected tripple backtick
    if re.match(r"^#{1,6} .+$", markdown) is not None:
        return BlockType.HEADING
    if re.match(r"^```\w*(?:\n.*)+\n```$", markdown):
        return BlockType.CODE
    if re.match(r"^(> .*\n?)+$", markdown):
        return BlockType.QUOTE
    if re.match(r"^(- .*\n?)+$", markdown):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
