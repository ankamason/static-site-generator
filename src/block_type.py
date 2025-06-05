from enum import Enum
import re


class BlockType(Enum):
    """Enumeration of supported markdown block types."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block (str): A single block of markdown text with leading/trailing whitespace stripped
        
    Returns:
        BlockType: The type of the block
        
    Block type rules:
    - Headings: Start with 1-6 # characters, followed by a space
    - Code blocks: Start and end with 3 backticks (```)
    - Quote blocks: Every line starts with >
    - Unordered lists: Every line starts with - followed by space
    - Ordered lists: Every line starts with number. followed by space, incrementing from 1
    - Paragraphs: Everything else
    """
    lines = block.split('\n')
    
    # Check for heading (1-6 # characters followed by space)
    if lines[0].startswith('#'):
        # Count consecutive # characters at the start
        hash_count = 0
        for char in lines[0]:
            if char == '#':
                hash_count += 1
            else:
                break
        
        # Must be 1-6 # characters followed by a space
        if 1 <= hash_count <= 6 and len(lines[0]) > hash_count and lines[0][hash_count] == ' ':
            return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if len(lines) >= 2 and lines[0].startswith('```') and lines[-1].endswith('```'):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (every line starts with number. followed by space, incrementing from 1)
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph if none of the above match
    return BlockType.PARAGRAPH


def _is_ordered_list(lines):
    """
    Helper function to check if lines form a valid ordered list.
    
    Args:
        lines (list[str]): List of lines to check
        
    Returns:
        bool: True if lines form a valid ordered list
    """
    for i, line in enumerate(lines):
        # Expected number for this line (1-indexed)
        expected_num = i + 1
        
        # Check if line starts with expected number followed by '. '
        expected_prefix = f"{expected_num}. "
        if not line.startswith(expected_prefix):
            return False
    
    return True
