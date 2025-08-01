class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        props = ""
        for key, value in self.props.items():
            props = props + " " + f'{key}="{value}"'

        return props

    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props=props or {})

    def to_html(self):
        if self.value is None:
            raise ValueError("ERROR: Node has no value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props or {})

    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: Parent node object does not have a tag")
        elif not self.children:
            raise ValueError("Error: Parent node has no children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html = html + f"{child.to_html()}"
        html += f"</{self.tag}>"

        return html
