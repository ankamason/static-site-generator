from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    """
    Split TextNodes containing image markdown into separate TextNodes.
    
    Takes a list of TextNodes and splits any NORMAL nodes that contain
    markdown image syntax ![alt](url) into separate nodes:
    - Normal text becomes TextNode with TextType.NORMAL
    - Image markdown becomes TextNode with TextType.IMAGE and URL
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list with image markdown split into separate nodes
        
    Examples:
        Input: [TextNode("Text ![img](url) more", TextType.NORMAL)]
        Output: [
            TextNode("Text ", TextType.NORMAL),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" more", TextType.NORMAL)
        ]
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process NORMAL text nodes - leave others unchanged
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from this node
        images = extract_markdown_images(old_node.text)
        
        # If no images found, keep original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process each image found
        current_text = old_node.text
        
        for image_alt, image_url in images:
            # Create the full markdown syntax to split on
            image_markdown = f"![{image_alt}]({image_url})"
            
            # Split text at this image (maxsplit=1 to handle one at a time)
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if our extraction worked correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the image (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.NORMAL))
            
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Continue processing with the text after this image
            current_text = after_text
        
        # Add any remaining text after all images (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
    
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Split TextNodes containing link markdown into separate TextNodes.
    
    Takes a list of TextNodes and splits any NORMAL nodes that contain
    markdown link syntax [text](url) into separate nodes:
    - Normal text becomes TextNode with TextType.NORMAL
    - Link markdown becomes TextNode with TextType.LINK and URL
    
    Args:
        old_nodes (list): List of TextNode objects to process
        
    Returns:
        list: New list with link markdown split into separate nodes
        
    Examples:
        Input: [TextNode("Text [link](url) more", TextType.NORMAL)]
        Output: [
            TextNode("Text ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" more", TextType.NORMAL)
        ]
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process NORMAL text nodes - leave others unchanged
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from this node
        links = extract_markdown_links(old_node.text)
        
        # If no links found, keep original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process each link found
        current_text = old_node.text
        
        for link_text, link_url in links:
            # Create the full markdown syntax to split on
            link_markdown = f"[{link_text}]({link_url})"
            
            # Split text at this link (maxsplit=1 to handle one at a time)
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                # This shouldn't happen if our extraction worked correctly
                continue
            
            before_text, after_text = sections
            
            # Add the text before the link (if not empty)
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.NORMAL))
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Continue processing with the text after this link
            current_text = after_text
        
        # Add any remaining text after all links (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
    
    return new_nodes
