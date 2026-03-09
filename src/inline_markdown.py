import re
from enum import Enum
from textnode import TextType, TextNode

class MarkdownType(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

def split_nodes_delimiter(old_nodes, delimiter, text_type): # old_nodes - List / delimiter - string / text_type - TextType
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter) # list of text that needs to become text Node
        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown syntax, formatted section not closed")
        for i in range(len(sections)):
            if sections[i]== "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern,text)
    return matches