import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            self.assertEqual("Node 3 should have failed",0)
        except Exception as e:
            self.assertEqual(e.args[0], "All leaf nodes must have value")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(),'LeafNode(p, Hello, world!, None)')
        self.assertEqual(node2.__repr__(),"LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node_failure = LeafNode("b", "")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        parent_node2 = ParentNode("",[child_node])
        try:
            parent_node2.to_html()
            self.assertEqual("Parent_Node2 should have failed",0)
        except Exception as e:
            self.assertEqual(e.args[0], "All Parent nodes must have a tag")
        parent_node3 = ParentNode("b",[])
        try:
            parent_node3.to_html()
            self.assertEqual("Parent_Node3 should have failed",0)
        except Exception as e:
            self.assertEqual(e.args[0], "All Parent node must have minimum 1 child")
        parent_node4 = ParentNode("b", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node4.to_html(), '<b href="https://www.google.com"><span>child</span></b>')
        parent_node5 = ParentNode("h", [child_node_failure])
        try:
            parent_node5.to_html()
            self.assertEqual("Parent_node5 children should have failed",0)
        except Exception as e:
            self.assertEqual(e.args[0], "All leaf nodes must have value")

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_failure = LeafNode("b", "")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("div", [grandchild_node_failure])
        child_parent_failure = ParentNode("", [child_node])
        child_parent_tag = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("span", [child_node2])
        parent_node3 = ParentNode("div", [child_parent_failure])
        parent_node4 = ParentNode("div", [child_parent_tag])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        try:
            parent_node2.to_html()
            self.assertEqual("Parent_node2 grandchildren shoudl have failed",0)
        except Exception as e:
            self.assertEqual(e.args[0], "All leaf nodes must have value")
        try:
            child_parent_failure.to_html()
            self.assertEqual("parent in child_parent_failure should have failed")
        except Exception as e:
            self.assertEqual(e.args[0], "All Parent nodes must have a tag")
        try:
            parent_node3.to_html()
            self.assertEqual("child in child_parent_failure should have failed")
        except Exception as e:
            self.assertEqual(e.args[0], "All Parent nodes must have a tag")
        self.assertEqual(
            child_parent_tag.to_html(),
            '<a href="https://www.google.com"><span><b>grandchild</b></span></a>'
        )
        self.assertEqual(
            parent_node4.to_html(),
            '<div><a href="https://www.google.com"><span><b>grandchild</b></span></a></div>'
        )
        
        




if __name__ == "__main__":
    unittest.main()