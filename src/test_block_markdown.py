import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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

    def test_markdown_to_html_codeblock(self):
        # self.skipTest("testing purposes")
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_paragraph(self):
        # self.skipTest("testing purposes")
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_markdown_to_html_headings(self):
        # self.skipTest("testing purposes")
        md = "# **bold** Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1><b>bold</b> Heading 1</h1></div>"
        )
        md6 = """###### _italic_ heading 6

        ##### heading 5

        #### heading 4

        ### heading 3

        ## heading 2

        # heading 1

        ####### paragraph
        """
        node = markdown_to_html_node(md6)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6><i>italic</i> heading 6</h6><h5>heading 5</h5><h4>heading 4</h4><h3>heading 3</h3><h2>heading 2</h2><h1>heading 1</h1><p>####### paragraph</p></div>"
        )

    def test_markdown_to_html_quotes(self):
        # self.skipTest("testing purposes")
        md = """> quote1
>quote2
>quote3

> outside quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote1 quote2 quote3</blockquote><blockquote>outside quote</blockquote></div>"
        )
    
    def test_markdown_to_html_ordered_list(self):
        # self.skipTest("testing purposes")
        md = """1. list 1
2. list 2
3. list 3
4. list 4

Not a list only a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list 1</li><li>list 2</li><li>list 3</li><li>list 4</li></ol><p>Not a list only a paragraph</p></div>"
        )

    def test_markdown_to_html_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3
- Item 4

1. O Item 1
2. O Item 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li></ul><ol><li>O Item 1</li><li>O Item 2</li></ol></div>"
        )