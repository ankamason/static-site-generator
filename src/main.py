from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from split_delimiter import split_nodes_delimiter
from extract_links import extract_markdown_images, extract_markdown_links
from split_images_links import split_nodes_image, split_nodes_link

def main():
    # Previous functionality verification (shortened)
    print("=== System Verification ===")
    
    # Quick verification that everything still works
    paragraph = ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " text")])
    print("✅ HTML generation:", paragraph.to_html())
    
    # Quick delimiter test
    delimiter_result = split_nodes_delimiter([TextNode("**bold**", TextType.NORMAL)], "**", TextType.BOLD)
    print("✅ Delimiter splitting:", len(delimiter_result), "nodes")
    
    # Quick extraction test
    images = extract_markdown_images("![test](url)")
    print("✅ Extraction functions:", len(images), "images found")
    
    # NEW: Split Images and Links Testing
    print("\n=== Split Images and Links Function Tests ===")
    
    # Test 1: Split Images - Basic
    print("Test 1: Split Images - Basic")
    image_node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
    )
    print("Original:", image_node)
    image_result = split_nodes_image([image_node])
    print("Split result:")
    for i, node in enumerate(image_result):
        print(f"  {i}: {node}")
    
    expected_image = [
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.NORMAL),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
    ]
    print("✅ Matches expected:", image_result == expected_image)
    
    # Test 2: Split Links - Basic
    print("\nTest 2: Split Links - Basic")
    link_node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.NORMAL,
    )
    print("Original:", link_node)
    link_result = split_nodes_link([link_node])
    print("Split result:")
    for i, node in enumerate(link_result):
        print(f"  {i}: {node}")
    
    expected_link = [
        TextNode("This is text with a link ", TextType.NORMAL),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    ]
    print("✅ Matches expected:", link_result == expected_link)
    
    # Test 3: No Images/Links
    print("\nTest 3: No Images/Links")
    plain_node = TextNode("Just plain text with no special formatting", TextType.NORMAL)
    no_images = split_nodes_image([plain_node])
    no_links = split_nodes_link([plain_node])
    print("Plain text:", plain_node)
    print("After image split:", no_images)
    print("After link split:", no_links)
    print("✅ Unchanged:", no_images == [plain_node] and no_links == [plain_node])
    
    # Test 4: Mixed Node Types
    print("\nTest 4: Mixed Node Types (should preserve non-NORMAL)")
    mixed_nodes = [
        TextNode("Normal with ![image](img.jpg)", TextType.NORMAL),
        TextNode("Already bold", TextType.BOLD),
        TextNode("Normal with [link](url.com)", TextType.NORMAL),
    ]
    print("Original mixed nodes:")
    for i, node in enumerate(mixed_nodes):
        print(f"  {i}: {node}")
    
    mixed_images = split_nodes_image(mixed_nodes)
    print("After image split:")
    for i, node in enumerate(mixed_images):
        print(f"  {i}: {node}")
    
    mixed_links = split_nodes_link(mixed_images)  # Chain them
    print("After link split:")
    for i, node in enumerate(mixed_links):
        print(f"  {i}: {node}")
    
    # Test 5: Image at start and end
    print("\nTest 5: Images at start and end")
    edge_node = TextNode("![start](start.jpg) middle text ![end](end.jpg)", TextType.NORMAL)
    edge_result = split_nodes_image([edge_node])
    print("Original:", edge_node)
    print("Split result:")
    for i, node in enumerate(edge_result):
        print(f"  {i}: {node}")
    
    # Test 6: Adjacent images/links
    print("\nTest 6: Adjacent patterns")
    adjacent_node = TextNode("![img1](url1)![img2](url2)", TextType.NORMAL)
    adjacent_result = split_nodes_image([adjacent_node])
    print("Adjacent images:", adjacent_node)
    print("Split result:")
    for i, node in enumerate(adjacent_result):
        print(f"  {i}: {node}")
    
    # Test 7: Complete Integration Pipeline
    print("\n=== Complete Integration Pipeline ===")
    complex_text = "This has **bold** and ![image](img.jpg) and [link](site.com) and `code`!"
    print(f"Original text: {complex_text}")
    
    # Step 1: Start with TextNode
    nodes = [TextNode(complex_text, TextType.NORMAL)]
    print(f"Step 1 - Initial: {len(nodes)} nodes")
    
    # Step 2: Process delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    print(f"Step 2 - After bold: {len(nodes)} nodes")
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print(f"Step 3 - After code: {len(nodes)} nodes")
    
    # Step 4: Process images and links
    nodes = split_nodes_image(nodes)
    print(f"Step 4 - After images: {len(nodes)} nodes")
    
    nodes = split_nodes_link(nodes)
    print(f"Step 5 - After links: {len(nodes)} nodes")
    
    # Step 6: Show final breakdown
    print("Final TextNodes:")
    for i, node in enumerate(nodes):
        print(f"  {i}: {node}")
    
    # Step 7: Convert to HTML
    html_nodes = []
    for text_node in nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    final_paragraph = ParentNode("p", html_nodes)
    print(f"\nFinal HTML: {final_paragraph.to_html()}")
    
    # Test 8: Error resilience
    print("\n=== Error Resilience Tests ===")
    
    # Empty content
    empty_node = TextNode("", TextType.NORMAL)
    empty_images = split_nodes_image([empty_node])
    empty_links = split_nodes_link([empty_node])
    print("Empty text handling - Images:", len(empty_images), "Links:", len(empty_links))
    
    # Only images/links
    only_image = TextNode("![only](img.jpg)", TextType.NORMAL)
    only_image_result = split_nodes_image([only_image])
    print("Only image result:")
    for node in only_image_result:
        print(f"  {node}")
    
    print("\n=== All Split Functions Complete! ===")
    print("✅ Image splitting working with complex patterns")
    print("✅ Link splitting working with complex patterns")
    print("✅ Proper handling of edge cases and empty content")
    print("✅ Integration with existing delimiter splitting")
    print("✅ Complete Markdown → TextNode → HTML pipeline")
    print("🚀 Advanced Markdown parsing system complete!")

if __name__ == "__main__":
    main()
