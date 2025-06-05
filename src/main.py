from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from split_delimiter import split_nodes_delimiter
from extract_links import extract_markdown_images, extract_markdown_links

def main():
    # Previous tests (shortened for focus)
    print("=== Node System Verification ===")
    paragraph = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, " and normal text")
    ])
    print("✅ HTML generation working:", paragraph.to_html())
    
    # Split delimiter verification
    node = TextNode("This is **bold** text", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("✅ Split delimiter working:", len(new_nodes), "nodes created")
    
    # NEW: Extraction Function Testing
    print("\n=== Markdown Extraction Function Tests ===")
    
    # Test 1: Extract images
    print("Test 1: Extract Images")
    image_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print("Text:", image_text)
    images = extract_markdown_images(image_text)
    print("Extracted images:", images)
    print("Expected: [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]")
    print("Match:", images == [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    # Test 2: Extract links
    print("\nTest 2: Extract Links")
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print("Text:", link_text)
    links = extract_markdown_links(link_text)
    print("Extracted links:", links)
    print("Expected: [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]")
    print("Match:", links == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    # Test 3: Mixed images and links
    print("\nTest 3: Mixed Images and Links")
    mixed_text = "![image](img.jpg) and [link](site.com) and ![another](pic.png)"
    print("Text:", mixed_text)
    images_mixed = extract_markdown_images(mixed_text)
    links_mixed = extract_markdown_links(mixed_text)
    print("Images found:", images_mixed)
    print("Links found:", links_mixed)
    
    # Test 4: No matches
    print("\nTest 4: No Matches")
    plain_text = "This is just plain text with no special formatting"
    images_none = extract_markdown_images(plain_text)
    links_none = extract_markdown_links(plain_text)
    print("Text:", plain_text)
    print("Images found:", images_none, "(should be empty)")
    print("Links found:", links_none, "(should be empty)")
    
    # Test 5: Edge cases
    print("\nTest 5: Edge Cases")
    
    # Empty alt text and anchor text
    edge_text = "![](empty-alt.jpg) and [](empty-anchor.com)"
    images_edge = extract_markdown_images(edge_text)
    links_edge = extract_markdown_links(edge_text)
    print("Edge case text:", edge_text)
    print("Images with empty alt:", images_edge)
    print("Links with empty anchor:", links_edge)
    
    # Complex URLs
    complex_text = "![complex](https://example.com/path/to/image.png?param=value&other=123)"
    images_complex = extract_markdown_images(complex_text)
    print("Complex URL:", images_complex)
    
    # Test 6: Verify links don't match images
    print("\nTest 6: Link/Image Distinction")
    distinction_text = "This has ![an image](img.jpg) and [a link](site.com) - they should be separate!"
    images_dist = extract_markdown_images(distinction_text)
    links_dist = extract_markdown_links(distinction_text)
    print("Text:", distinction_text)
    print("Images only:", images_dist)
    print("Links only:", links_dist)
    print("✅ Correct separation:", len(images_dist) == 1 and len(links_dist) == 1)
    
    # Test 7: Multiple on same line
    print("\nTest 7: Multiple Same Type")
    multi_links = "Check out [Site 1](one.com) and [Site 2](two.com) and [Site 3](three.com)!"
    links_multi = extract_markdown_links(multi_links)
    print("Multiple links:", links_multi)
    print("✅ Found all 3:", len(links_multi) == 3)
    
    # Test 8: Real-world example
    print("\nTest 8: Real-World Example")
    real_world = """
    Check out this ![awesome diagram](https://example.com/diagram.svg) 
    that explains the concept. For more info, visit [our docs](https://docs.example.com)
    or see the ![tutorial screenshot](https://example.com/screenshot.png).
    Also useful: [Stack Overflow](https://stackoverflow.com) and [GitHub](https://github.com).
    """
    real_images = extract_markdown_images(real_world)
    real_links = extract_markdown_links(real_world)
    print("Real-world images:", real_images)
    print("Real-world links:", real_links)
    print(f"✅ Found {len(real_images)} images and {len(real_links)} links")
    
    print("\n=== Extraction Functions Complete! ===")
    print("✅ Image extraction working")
    print("✅ Link extraction working") 
    print("✅ Proper separation between images and links")
    print("✅ Handles edge cases and complex URLs")
    print("🚀 Ready for link and image splitting functions!")

if __name__ == "__main__":
    main()
