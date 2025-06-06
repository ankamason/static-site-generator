from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from text_to_textnodes import text_to_textnodes
from markdown_to_blocks import markdown_to_blocks
from block_type import BlockType, block_to_block_type


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown (str): Raw markdown text representing a full document
        
    Returns:
        ParentNode: A div containing all the converted HTML blocks
    """
    # Step 1: Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Handle empty markdown - create div with empty paragraph
    if not blocks:
        empty_paragraph = ParentNode("p", [LeafNode(None, "")])
        return ParentNode("div", [empty_paragraph])
    
    # Step 2: Convert each block to an HTMLNode
    block_nodes = []
    for block in blocks:
        # Determine the type of this block
        block_type = block_to_block_type(block)
        
        # Convert block to appropriate HTMLNode based on type
        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)
        else:
            # Fallback to paragraph for unknown types
            block_node = paragraph_to_html_node(block)
        
        block_nodes.append(block_node)
    
    # Step 3: Wrap all blocks in a parent div
    return ParentNode("div", block_nodes)


def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    
    This is the shared function that handles inline formatting for most block types.
    
    Args:
        text (str): Text that may contain inline markdown
        
    Returns:
        list[HTMLNode]: List of HTMLNode objects representing the inline content
    """
    # Use existing pipeline: text -> TextNodes -> HTMLNodes
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode.
    
    Args:
        block (str): Paragraph block text
        
    Returns:
        ParentNode: A <p> tag containing the paragraph content
    """
    # Convert newlines within paragraph to spaces (standard markdown behavior)
    paragraph_text = block.replace('\n', ' ')
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """
    Convert a heading block to an HTMLNode.
    
    Args:
        block (str): Heading block text (e.g., "# Heading" or "## Subheading")
        
    Returns:
        ParentNode: An <h1> through <h6> tag containing the heading content
    """
    # Count the number of # characters to determine heading level
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # Extract the heading text (everything after "# ")
    heading_text = block[level + 1:]  # +1 to skip the space after #
    
    # Convert inline markdown in the heading text
    children = text_to_children(heading_text)
    
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """
    Convert a code block to an HTMLNode.
    
    Code blocks are special - they should NOT process inline markdown.
    
    Args:
        block (str): Code block text including ``` delimiters
        
    Returns:
        ParentNode: A <pre><code> structure containing the raw code
    """
    # Split into lines
    lines = block.split('\n')
    
    # Remove the opening ``` line (first line) and closing ``` line (last line)
    # Keep everything in between, including empty lines
    if len(lines) >= 3:  # At least opening, content, closing
        code_lines = lines[1:-1]
    elif len(lines) == 2:  # Just opening and closing
        code_lines = []
    else:  # Single line - shouldn't happen with valid code blocks
        code_lines = lines
    
    # Join the code lines back together with newlines
    # Add trailing newline if there was content
    if code_lines:
        code_content = '\n'.join(code_lines) + '\n'
    else:
        code_content = ''
    
    # Create a simple TextNode with the raw code (no inline processing)
    code_text_node = TextNode(code_content, TextType.NORMAL)
    code_html_node = text_node_to_html_node(code_text_node)
    
    # Wrap in <code> tag, then <pre> tag
    code_node = ParentNode("code", [code_html_node])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """
    Convert a quote block to an HTMLNode.
    
    Args:
        block (str): Quote block text with > prefixes
        
    Returns:
        ParentNode: A <blockquote> tag containing the quote content
    """
    # Remove the > prefix from each line
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        # Remove the > and any following space
        if line.startswith('> '):
            quote_lines.append(line[2:])  # Remove "> "
        elif line.startswith('>'):
            quote_lines.append(line[1:])  # Remove just ">"
        else:
            quote_lines.append(line)  # Shouldn't happen in valid quote
    
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """
    Convert an unordered list block to an HTMLNode.
    
    Args:
        block (str): Unordered list block text with - prefixes
        
    Returns:
        ParentNode: A <ul> tag containing <li> elements
    """
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the "- " prefix
        item_text = line[2:]  # Remove "- "
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """
    Convert an ordered list block to an HTMLNode.
    
    Args:
        block (str): Ordered list block text with number prefixes
        
    Returns:
        ParentNode: An <ol> tag containing <li> elements
    """
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the ". " and remove everything up to and including it
        dot_index = line.find('. ')
        item_text = line[dot_index + 2:]  # Remove "1. " or "2. " etc.
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)
