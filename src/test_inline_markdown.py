import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ],
            split_nodes_delimiter([node], "`", TextType.CODE)
        )
        node2 = TextNode("THis is not a text node with **bold** text", TextType.BOLD)
        self.assertEqual(
            [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("THis is not a text node with **bold** text", TextType.BOLD),
            ],
            split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        )
        node3 = TextNode("This is a text with a **bold block** word", TextType.TEXT)
        self.assertEqual(
            [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("THis is not a text node with **bold** text", TextType.BOLD),
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ],
            split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD)
        )
        node4 = TextNode("This is a text with a _italic block_ word", TextType.TEXT)
        node5 = TextNode("This is a second text with a _italic block 2_ word", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("This is a second text with a ", TextType.TEXT),
                TextNode("italic block 2", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            split_nodes_delimiter([node4, node5], "_", TextType.ITALIC)
        )
        node_f = TextNode("This is a failing text with _broken block word", TextType.TEXT)
        try:
            split_nodes_delimiter([node_f, node5], "_", TextType.ITALIC)
        except Exception as e:
            self.assertEqual(e.args[0],'Invalid Markdown syntax, formatted section not closed')
        
    def test_double_delimiter(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
        node2 = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes2, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes2,
        )

if __name__ == "__main__":
    unittest.main()