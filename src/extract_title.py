def extract_title(markdown):
    """
    Extract the h1 header from markdown text.
    
    This function looks for the first line that starts with a single '#'
    followed by a space, which represents an h1 header in markdown.
    
    Args:
        markdown (str): Raw markdown text
        
    Returns:
        str: The title text without the # and whitespace
        
    Raises:
        ValueError: If no h1 header is found
        
    Examples:
        >>> extract_title("# Hello World")
        "Hello World"
        >>> extract_title("# My Title\n\nSome content")
        "My Title"
        >>> extract_title("## Not h1")
        ValueError: No h1 header found
    """
    if not markdown or not markdown.strip():
        raise ValueError("No h1 header found in empty markdown")
    
    # Split markdown into lines for processing
    lines = markdown.split('\n')
    
    for line in lines:
        # Strip leading/trailing whitespace from each line
        stripped_line = line.strip()
        
        # Check if line starts with exactly one # followed by space
        if stripped_line.startswith('# '):
            # Extract title by removing '# ' and any extra whitespace
            title = stripped_line[2:].strip()  # Remove '# ' (2 characters)
            
            if title:  # Make sure there's actually text after the #
                return title
            else:
                raise ValueError("No h1 header found - found '# ' but no title text")
        
        # Check for invalid h1 (# without space)
        elif stripped_line.startswith('#') and len(stripped_line) > 1:
            # This catches cases like "#NoSpace" or "##Multiple"
            if not stripped_line.startswith('# '):
                continue  # Keep looking, this isn't a valid h1
    
    # If we get here, no h1 header was found
    raise ValueError("No h1 header found in markdown")
