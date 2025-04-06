import re

from typing import Sequence
from enum import Enum
from htmlnode import ParentNode, LeafNode
from text_converter import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HORIZONTAL_RULE = "horizontal rule"

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
    if re.match(r"^(?:>.*\n?)+$", markdown):
        return BlockType.QUOTE
    if re.match(r"^(?: *[*-] *){3,}$", markdown):
        return BlockType.HORIZONTAL_RULE
    if re.match(r"^(?:- .*\n?)+$", markdown):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(markdown):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_child_nodes(text: str) -> Sequence[LeafNode | ParentNode]:
    text_nodes = text_to_textnodes(text)
    child_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return child_nodes

def lines_to_list_items(lines: list[str]) -> list[ParentNode]:
    nodes = []
    for line in lines:
        nodes.append(ParentNode("li", text_to_child_nodes(line)))
    return nodes

def markdown_block_to_html(markdown: str) -> LeafNode | ParentNode:
    block_type = get_markdown_block_type(markdown)
    match block_type:
        case BlockType.HEADING:
            level, text = re.findall(r"^(#{1,6}) (.+)$", markdown, )[0]
            return ParentNode(f"h{len(level)}", text_to_child_nodes(text))
        case BlockType.QUOTE:
            text = " ".join([line.lstrip(">").strip() for line in markdown.split("\n")])
            return ParentNode("blockquote", text_to_child_nodes(text))
        case BlockType.CODE:
            text = markdown.strip("`\n")
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, text)])])
        case BlockType.ORDERED_LIST:
            lines = markdown.split("\n")
            text_lines = [". ".join(line.split(". ")[1:]) for line in lines]
            return ParentNode("ol", lines_to_list_items(text_lines))
        case BlockType.UNORDERED_LIST:
            lines = markdown.split("\n")
            text_lines = [line.lstrip("- ") for line in lines]
            return ParentNode("ul", lines_to_list_items(text_lines))
        case BlockType.HORIZONTAL_RULE:
            return LeafNode("hr", "")
        case _:
            return ParentNode("p", text_to_child_nodes(" ".join(markdown.split("\n"))))

def markdown_to_html_nodes(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    if len(blocks) == 0:
        raise ValueError("no valid markdown found")

    child_nodes = []
    for block in blocks:
        child_nodes.append(markdown_block_to_html(block))

    return ParentNode("div", child_nodes)

def extract_markdown_heading(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("title missing")