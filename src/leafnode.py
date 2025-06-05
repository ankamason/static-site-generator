from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        """
        Initialize a leaf node (HTML element with no children).
        
        Args:
            tag (str or None): HTML tag name (e.g., 'p', 'a', 'strong')
                              If None, renders as raw text
            value (str): Text content - REQUIRED for all leaf nodes
            props (dict, optional): HTML attributes as key-value pairs
        """
        # Call parent constructor: tag, value, children=None, props
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        """
        Convert this leaf node to HTML string.
        
        Returns:
            str: HTML string representation
            
        Raises:
            ValueError: If value is None (all leaf nodes must have content)
            
        Examples:
            LeafNode("p", "Hello") → "<p>Hello</p>"
            LeafNode(None, "Raw text") → "Raw text"
            LeafNode("a", "Link", {"href": "url"}) → '<a href="url">Link</a>'
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        # If no tag, return raw text
        if self.tag is None:
            return self.value
        
        # Generate HTML with tag and attributes
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
