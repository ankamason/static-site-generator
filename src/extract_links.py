import re

def extract_markdown_images(text):
    """
    Extract all markdown images from text and return list of (alt_text, url) tuples.
    
    Markdown image syntax: ![alt text](url)
    
    This function uses regex to find all instances of markdown image syntax
    and extracts both the alt text and URL from each match.
    
    Args:
        text (str): Raw markdown text to search
        
    Returns:
        list: List of tuples, each containing (alt_text, url)
        
    Examples:
        extract_markdown_images("![cat](cat.jpg) and ![dog](dog.png)")
        → [("cat", "cat.jpg"), ("dog", "dog.png")]
    """
    # Regex pattern explanation:
    # !\[        - Literal ![ (escaped brackets)
    # ([^\[\]]*) - Capture group 1: any characters except [ or ] (alt text)
    # \]         - Literal ] (escaped)
    # \(         - Literal ( (escaped)
    # ([^\(\)]*) - Capture group 2: any characters except ( or ) (URL)  
    # \)         - Literal ) (escaped)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # findall returns list of tuples with captured groups
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extract all markdown links from text and return list of (anchor_text, url) tuples.
    
    Markdown link syntax: [anchor text](url)
    
    This function uses regex to find all instances of markdown link syntax
    and extracts both the anchor text and URL from each match.
    
    Args:
        text (str): Raw markdown text to search
        
    Returns:
        list: List of tuples, each containing (anchor_text, url)
        
    Examples:
        extract_markdown_links("[Google](google.com) and [GitHub](github.com)")
        → [("Google", "google.com"), ("GitHub", "github.com")]
    """
    # Regex pattern explanation:
    # (?<!\!)    - Negative lookbehind: not preceded by ! (to avoid images)
    # \[         - Literal [ (escaped)
    # ([^\[\]]*) - Capture group 1: any characters except [ or ] (anchor text)
    # \]         - Literal ] (escaped)
    # \(         - Literal ( (escaped)
    # ([^\(\)]*) - Capture group 2: any characters except ( or ) (URL)
    # \)         - Literal ) (escaped)
    pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    # findall returns list of tuples with captured groups
    matches = re.findall(pattern, text)
    return matches
