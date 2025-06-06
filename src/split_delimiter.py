from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes based on delimiter markers.
    
    Takes a list of TextNodes and returns a new list where TextNodes with
    TextType.NORMAL are split based on the delimiter, creating new TextNodes
    with the specified text_type for content between delimiters.
    
    Args:
        old_nodes (list[TextNode]): List of TextNodes to process
        delimiter (str): The delimiter to split on (e.g., "**", "*", "`")
        text_type (TextType): The TextType to assign to delimited content
        
    Returns:
        list[TextNode]: New list with split TextNodes
        
    Raises:
        ValueError: If delimiter is not properly closed in any text
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process NORMAL nodes, leave others unchanged
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Split this node's text by the delimiter
        split_result = split_single_node(old_node.text, delimiter, text_type)
        new_nodes.extend(split_result)
    
    return new_nodes


def split_single_node(text, delimiter, text_type):
    """
    Split a single text string by delimiter.
    
    Args:
        text (str): Text to split
        delimiter (str): Delimiter to split on
        text_type (TextType): Type for delimited content
        
    Returns:
        list[TextNode]: List of TextNodes from splitting the text
    """
    if delimiter not in text:
        # No delimiter found, return original as NORMAL
        return [TextNode(text, TextType.NORMAL)]
    
    nodes = []
    current_text = text
    
    while delimiter in current_text:
        # Find first occurrence of delimiter
        first_delimiter = current_text.find(delimiter)
        
        # Add text before first delimiter (if any)
        if first_delimiter > 0:
            before_text = current_text[:first_delimiter]
            nodes.append(TextNode(before_text, TextType.NORMAL))
        
        # Remove the part we've processed including first delimiter
        after_first = current_text[first_delimiter + len(delimiter):]
        
        # Find closing delimiter
        if delimiter not in after_first:
            # No closing delimiter - this is invalid markdown
            raise ValueError(f"Invalid Markdown syntax: unclosed delimiter '{delimiter}' in text '{text}'")
        
        second_delimiter = after_first.find(delimiter)
        
        # Extract content between delimiters
        delimited_content = after_first[:second_delimiter]
        nodes.append(TextNode(delimited_content, text_type))
        
        # Continue with remaining text after second delimiter
        current_text = after_first[second_delimiter + len(delimiter):]
    
    # Add any remaining text
    if current_text:
        nodes.append(TextNode(current_text, TextType.NORMAL))
    
    # Filter out empty text nodes
    return [node for node in nodes if node.text]
