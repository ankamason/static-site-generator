from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes on delimiter boundaries, converting delimited text to new text type.
    
    This function is the core of Markdown inline parsing. It can handle any
    delimiter-based formatting like **bold**, *italic*, `code`, etc.
    
    Args:
        old_nodes (list): List of TextNode objects to process
        delimiter (str): The delimiter to split on (e.g., "**", "*", "`")
        text_type (TextType): The text type for content inside delimiters
        
    Returns:
        list: New list of TextNode objects with delimited content converted
        
    Raises:
        ValueError: If delimiter is not properly closed (invalid Markdown)
        
    Examples:
        Input: [TextNode("This is **bold** text", TextType.NORMAL)]
        Delimiter: "**", TextType.BOLD
        Output: [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD), 
            TextNode(" text", TextType.NORMAL)
        ]
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process NORMAL text nodes - leave formatted nodes as-is
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Split the text on the delimiter
        parts = old_node.text.split(delimiter)
        
        # If only one part, no delimiter was found - keep original node
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
        
        # Check for unclosed delimiter (odd number of parts means unclosed)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unclosed delimiter '{delimiter}' in text '{old_node.text}'")
        
        # Process the parts alternating between normal and delimited text
        for i, part in enumerate(parts):
            # Skip empty parts (happens when delimiter is at start/end)
            if part == "":
                continue
            
            if i % 2 == 0:
                # Even indices are normal text (outside delimiters)
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
                # Odd indices are delimited text (inside delimiters)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes
