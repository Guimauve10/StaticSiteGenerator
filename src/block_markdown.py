from enum import Enum

from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown):
    split_newline = markdown.split("\n")

    if markdown.startswith("```") and markdown.endswith("```") and len(split_newline) > 1:
        return BlockType.CODE
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if markdown.startswith("1. "):
        for i in range(len(split_newline)):
            if not split_newline[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    if markdown.startswith("- "):
        for line in split_newline:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown.startswith(">"):
        for line in split_newline:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown): # match case could all be seperated into their own function and the inside of the for block could also be another helper function for ease of readability
    blocks = markdown_to_blocks(markdown)
    list_of_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_node = ParentNode("p", [])
                text = block.replace("\n", " ")
                block_node.children.extend(text_to_children(text))
                list_of_nodes.append(block_node)

            case BlockType.HEADING:
                split_space = block.split(" ")
                number_heading = len(split_space[0])
                text = " ".join(split_space[1:])
                block_node = ParentNode(f"h{number_heading}", [])
                block_node.children.extend(text_to_children(text))
                list_of_nodes.append(block_node)

            case BlockType.CODE:
                node = ParentNode("code", [])
                split_newline = block.split("\n")
                text = block[4:-3]
                text_node = TextNode(text, TextType.TEXT)
                node.children.append(text_node_to_html_node(text_node))
                block_node = ParentNode("pre", [node])
                list_of_nodes.append(block_node)

            case BlockType.QUOTE:
                block_node = ParentNode("blockquote", [])
                split_newline = block.split("\n")
                new_lines = []
                for line in split_newline:
                    new_line = line.replace("> ","")
                    new_line = new_line.replace(">", "")
                    new_lines.append(new_line)
                text = " ".join(new_lines)
                block_node.children.extend(text_to_children(text))
                list_of_nodes.append(block_node)

            case BlockType.UNORDERED_LIST:
                block_node = ParentNode("ul", [])
                split_newline = block.split("\n")
                for line in split_newline:
                    node = ParentNode("li", [])
                    text = line.replace("- ", "")
                    node.children.extend(text_to_children(text))
                    block_node.children.append(node)
                list_of_nodes.append(block_node)

            case BlockType.ORDERED_LIST:
                block_node = ParentNode("ol", [])
                split_newline = block.split("\n")
                i = 1
                for line in split_newline:
                    node = ParentNode("li", [])
                    text = line.replace(f"{i}. ", "")
                    node.children.extend(text_to_children(text))
                    block_node.children.append(node)
                    i += 1
                list_of_nodes.append(block_node)

    return ParentNode("div", list_of_nodes)

def text_to_children(text):
    list_of_children = []
    list_of_textnodes = text_to_textnodes(text)
    for node in list_of_textnodes:
        list_of_children.append(text_node_to_html_node(node))
    return list_of_children