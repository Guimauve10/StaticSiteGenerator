import re

from enum import Enum

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
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown):
    split_newline = markdown.split("\n")

    if markdown.startswith("```") and markdown.endswith("```") and len(split_newline) > 1:
        return BlockType.CODE
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")) and len(split_newline) == 1:
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