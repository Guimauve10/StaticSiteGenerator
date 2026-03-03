import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is some text unrelated", TextType.TEXT, "Boot.dev")
        self.assertNotEqual(node, node3)
        node4 = TextNode("Text", TextType.BOLD)
        node5 = TextNode("This is a text node", TextType.LINKS)
        node6 = TextNode("This is some text unrelated", TextType.TEXT, "hotmail.com")
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertNotEqual(node3, node6)


if __name__ == "__main__":
    unittest.main()