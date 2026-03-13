import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md2 = '      This is some text with extra white text before and after and just one paragraph      '
        blocks = markdown_to_blocks(md2)
        self.assertEqual(
            blocks,
            [
                'This is some text with extra white text before and after and just one paragraph',
            ]
        )

    def test_block_to_block_type_headings(self):
        md_headings = "### this is a heading 3"
        block_type = block_to_block_type(md_headings)
        self.assertEqual(block_type,BlockType.HEADING)
        md_headings2 = "###### this is a  heading 6"
        block_type = block_to_block_type(md_headings2)
        self.assertEqual(block_type,BlockType.HEADING)
        md_headings3 = "#This is not a valid heading"
        block_type = block_to_block_type(md_headings3)
        self.assertNotEqual(block_type,BlockType.HEADING)
        md_heading4 = "####### this is not a valid heading"
        block_type = block_to_block_type(md_heading4)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md_code = """```
This is code
        ```"""
        block_type = block_to_block_type(md_code)
        self.assertEqual(block_type, BlockType.CODE)
        md_code2 = "``````"
        block_type = block_to_block_type(md_code2)
        self.assertNotEqual(block_type, BlockType.CODE)
        md_code3 = "```\n```"
        block_type = block_to_block_type(md_code3)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_ordered_list(self):
        md_ordered_list = """1. Item 1
2. Item 2
3. Item 3"""
        block_type = block_to_block_type(md_ordered_list)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        md_ordered_list2 = "1.Item 1 not valid"
        block_type = block_to_block_type(md_ordered_list2)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        md_ordered_list3 = "1. Item solo"
        block_type = block_to_block_type(md_ordered_list3)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        md_ordered_list4 = "1. Item fails\na. Fails"
        block_type = block_to_block_type(md_ordered_list4)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_unordered_list(self):
        md_unordered_list = """- This is a list
- with items"""
        block_type = block_to_block_type(md_unordered_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        md_unordered_list2 = """- This is a list
-which fails"""
        block_type = block_to_block_type(md_unordered_list2)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_quote(self):
        md_quote = "> This is a quote 1"
        block_type = block_to_block_type(md_quote)
        self.assertEqual(block_type,BlockType.QUOTE)
        md_quote2 = ">This is another quote 2"
        block_type = block_to_block_type(md_quote2)
        self.assertEqual(block_type,BlockType.QUOTE)
        md_quote3 = "t>This is not a quote"
        block_type = block_to_block_type(md_quote3)
        self.assertNotEqual(block_type,BlockType.QUOTE)

    def test_block_to_block_paragraph(self):
        md_paragraph = "This is a basic paragraph with nothing special"
        block_type = block_to_block_type(md_paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        md_paragraph2 = "#This is not a valid paragraph"
        block_type = block_to_block_type(md_paragraph2)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        block_type = block_to_block_type(md_paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)