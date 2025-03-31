import re

from textnode import TextNode, TextType
from htmlnode import LeafNode
from markdown_converter import extract_markdown_images, extract_markdown_links

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("unmatched delimiter in Markdown text")
        for i in range(0, len(split_text) - 1, 2):
            if split_text[i] != '':
                new_nodes.append(TextNode(split_text[i], TextType.PLAIN))
            if split_text[i+1] != '':
                new_nodes.append(TextNode(split_text[i+1], text_type))
        if split_text[-1] != '':
            new_nodes.append(TextNode(split_text[-1], TextType.PLAIN))

    return new_nodes

def split_url_nodes(extractor: callable, markdown_formater: callable, text_type: TextType) -> callable:
    def split_url_nodes_by_type(old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.PLAIN:
                new_nodes.append(node)
                continue
            current_text = node.text
            matches = extractor(current_text)
            for match in matches:
                split_text = current_text.split(markdown_formater(match), maxsplit=1)
                if split_text[0] != '':
                    new_nodes.append(TextNode(split_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(match[0], text_type, match[1]))
                current_text = split_text[1]
            if current_text != '':
                new_nodes.append(TextNode(current_text, TextType.PLAIN))

        return new_nodes
    return split_url_nodes_by_type

def extract_markdown_images(markdown: str) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", markdown)

def extract_markdown_links(markdown: str) -> list[tuple]:
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", markdown)

split_nodes_image = split_url_nodes(extract_markdown_images, lambda image: f"![{image[0]}]({image[1]})", TextType.IMAGE)
split_nodes_link = split_url_nodes(extract_markdown_links, lambda link: f"[{link[0]}]({link[1]})", TextType.LINK)

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text.strip(), TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
