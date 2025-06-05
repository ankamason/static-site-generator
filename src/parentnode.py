from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        """
        Initialize a parent node (HTML element that contains other elements).
        
        Args:
            tag (str): HTML tag name - REQUIRED (e.g., 'div', 'p', 'ul')
            children (list): List of HTMLNode objects - REQUIRED
            props (dict, optional): HTML attributes as key-value pairs
        
        Note: ParentNode cannot have a value - it only contains children
        """
        # Call parent constructor: tag, value=None, children, props
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        """
        Convert this parent node and all its children to HTML string.
        
        This method recursively calls to_html() on each child node,
        combining the results into a complete HTML structure.
        
        Returns:
            str: Complete HTML string with opening tag, children content, closing tag
            
        Raises:
            ValueError: If tag is None (all parent nodes must have a tag)
            ValueError: If children is None or empty (parent nodes must contain elements)
            
        Examples:
            ParentNode("div", [LeafNode("p", "text")]) 
            → "<div><p>text</p></div>"
            
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")])
            ]) → "<ul><li>Item 1</li><li>Item 2</li></ul>"
        """
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
        
        # Return complete HTML structure
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
