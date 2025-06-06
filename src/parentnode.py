from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # Validate required tag
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        # Validate required children
        if self.children is None:
            raise ValueError("All parent nodes must have children")

        # Handle edge case of empty children list
        if len(self.children) == 0:
            raise ValueError("All parent nodes must have children")

        # Recursively generate HTML for all children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
