import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()