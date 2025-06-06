from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter
from split_images_links import split_nodes_image, split_nodes_link


def text_to_textnodes(text):
    """
    Convert a raw string of markdown text into a list of TextNode objects.
    
    Args:
        text (str): Raw markdown text to parse
        
    Returns:
        list[TextNode]: List of TextNode objects representing the parsed markdown
    """
    # Start with a single NORMAL TextNode containing all the text
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Process delimiter-based formatting in order of precedence
    # IMPORTANT: Process ** BEFORE * to handle nested cases correctly
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Process images and links (after delimiters to handle precedence correctly)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
