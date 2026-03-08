import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is some text unrelated", TextType.TEXT, "Boot.dev")
        self.assertNotEqual(node, node3)
        node4 = TextNode("Text", TextType.BOLD)
        node5 = TextNode("This is a text node", TextType.LINK)
        node6 = TextNode("This is some text unrelated", TextType.TEXT, "hotmail.com")
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertNotEqual(node3, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        node3 = TextNode("This is a italic text node", TextType.ITALIC)
        node4 = TextNode("This is a code text node", TextType.CODE)
        node5 = TextNode("This is a link text node", TextType.LINK, "Boot.dev")
        node6 = TextNode("This is a image text node", TextType.IMAGE, "Boot.dev")
        node7 = TextNode("This should fail", "Error")
        html_node = text_node_to_html_node(node)
        html_node_b = text_node_to_html_node(node2)
        html_node_i = text_node_to_html_node(node3)
        html_node_code = text_node_to_html_node(node4)
        html_node_a = text_node_to_html_node(node5)
        html_node_img = text_node_to_html_node(node6)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node_b.to_html(), "<b>This is a bold text node</b>")
        self.assertEqual(html_node_i.to_html(),"<i>This is a italic text node</i>")
        self.assertEqual(html_node_code.to_html(),"<code>This is a code text node</code>")
        self.assertEqual(html_node_a.to_html(),'<a href="Boot.dev">This is a link text node</a>')
        self.assertEqual(html_node_img.value, "")
        self.assertEqual(html_node_img.to_html(),'<img src="Boot.dev" alt="This is a image text node"></img>')
        try:
            html_node_failure = text_node_to_html_node(node7)
        except Exception as e:
            self.assertEqual(e.args[0],"Not valid text_type in text node")



if __name__ == "__main__":
    unittest.main()