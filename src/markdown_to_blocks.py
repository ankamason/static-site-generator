def markdown_to_blocks(markdown):
    """
    Split a raw markdown string into a list of block strings.
    
    Blocks are separated by blank lines (double newlines). Each block represents
    a distinct structural element like a heading, paragraph, or list.
    
    Args:
        markdown (str): Raw markdown text representing a full document
        
    Returns:
        list[str]: List of block strings with whitespace stripped and empty blocks removed
        
    Example:
        >>> md = "# Heading\\n\\nParagraph text\\n\\n- List item"
        >>> blocks = markdown_to_blocks(md)
        >>> len(blocks)
        3
    """
    # Split the markdown by double newlines (blank lines)
    raw_blocks = markdown.split("\n\n")
    
    # Process each block: strip whitespace and filter out empty blocks
    blocks = []
    for block in raw_blocks:
        # Strip leading and trailing whitespace from the block
        stripped_block = block.strip()
        
        # Only include non-empty blocks
        if stripped_block:
            blocks.append(stripped_block)
    
    return blocks
