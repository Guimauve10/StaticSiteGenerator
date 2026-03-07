


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not Implemented")
    
    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""
        total = "" # All attributes will be added to this string
        for attribute in self.props:
            total += f' {attribute}="{self.props[attribute]}"'
        return total
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All Parent node must have minimum 1 child")
        total = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            total += child.to_html()
        total += f"</{self.tag}>"
        return total