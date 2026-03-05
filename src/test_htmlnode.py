import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        dic_props = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        compare = ' href="https://www.google.com" target="_blank"'
        none_props = {}
        list = []
        node = HTMLNode("h1", "This is a header 1", [], dic_props) 
        list.append(node)
        node2 = HTMLNode("a", "This is a link", list, dic_props)
        list.append(node2)
        node3 = HTMLNode()
        node4 = HTMLNode(props=none_props)
        node6 = HTMLNode(props={
            "href": "https://www.google.com",
        })

        self.assertEqual(node.props_to_html(), compare)
        self.assertEqual(node2.props_to_html(), compare)
        self.assertNotEqual(node3.props_to_html(), compare)
        self.assertEqual(node3.props_to_html(), node4.props_to_html())
        self.assertNotEqual(node.props_to_html(), node6.props_to_html())

    def test_values(self):
        node = HTMLNode(
            "h1",
            "This is a header 1",
        )
        self.assertEqual(
            node.tag,
            "h1"
        )
        self.assertEqual(
            node.value,
            "This is a header 1",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None
        )

    def test_repr(self):
        node2 = HTMLNode()
        node = HTMLNode(
            "p",
            "Testing the tests",
            [node2],
            {
            "test" : "This is a major attribute test",
            "what" : "Adding more attributes",
            "Too many" : "Not Enough",
            "href": "Boot.dev",
        },
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Testing the tests, children: [HTMLNode(None, None, children: None, None)], {'test': 'This is a major attribute test', 'what': 'Adding more attributes', 'Too many': 'Not Enough', 'href': 'Boot.dev'})"
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node3 = LeafNode("b", "")
        node4 = LeafNode("", "There is no tag text")
        self.assertEqual(node4.to_html(), "There is no tag text")
        try:
            node3.to_html()
        except Exception as e:
            self.assertEqual(e.args[0], "All leaf nodes must have value")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(),'LeafNode(p, Hello, world!, None)')
        self.assertEqual(node2.__repr__(),"LeafNode(a, Click me!, {'href': 'https://www.google.com'})")


if __name__ == "__main__":
    unittest.main()