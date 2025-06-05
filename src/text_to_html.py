from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    """
    Convert a TextNode to appropriate HTMLNode (LeafNode).
    
    This function is the bridge between content parsing and HTML generation.
    It takes parsed text content (TextNode) and converts it to renderable
    HTML elements (LeafNode).
    
    Args:
        text_node (TextNode): The text node to convert
        
    Returns:
        LeafNode: Appropriate HTML node for the text type
        
    Raises:
        ValueError: If text_node has an unknown TextType
        
    Examples:
        TextNode("Hello", TextType.TEXT) → LeafNode(None, "Hello")
        TextNode("Bold", TextType.BOLD) → LeafNode("b", "Bold")
        TextNode("Link", TextType.LINK, "url") → LeafNode("a", "Link", {"href": "url"})
    """
    if text_node.text_type == TextType.NORMAL:
        # Raw text with no HTML tags
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        # Bold text: <b>text</b>
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        # Italic text: <i>text</i>
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        # Inline code: <code>text</code>
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        # Link: <a href="url">text</a>
        if text_node.url is None:
            raise ValueError("Link nodes must have a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        # Image: <img src="url" alt="text">
        if text_node.url is None:
            raise ValueError("Image nodes must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    else:
        # Unknown text type - this should never happen with proper enum usage
        raise ValueError(f"Unknown TextType: {text_node.text_type}")
