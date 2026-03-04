


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