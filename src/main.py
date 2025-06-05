from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node

def main():
    # Test TextNode (existing functionality)
    print("=== TextNode Tests ===")
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    
    # Test HTMLNode (existing functionality)
    print("\n=== HTMLNode Tests ===")
    html_node = HTMLNode(
        tag="a",
        value="Click me!",
        props={"href": "https://www.google.com", "target": "_blank"}
    )
    print("HTML Node:", html_node)
    print("Props to HTML:", repr(html_node.props_to_html()))
    
    # Test LeafNode functionality
    print("\n=== LeafNode Tests ===")
    p_node = LeafNode("p", "This is a paragraph of text.")
    print("Paragraph HTML:", p_node.to_html())
    
    link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print("Link HTML:", link_node.to_html())
    
    # Test ParentNode functionality
    print("\n=== ParentNode Tests ===")
    multi_parent = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ])
    print("Multi-child parent HTML:", multi_parent.to_html())
    
    # Test TextNode to HTMLNode conversion (NEW!)
    print("\n=== TextNode to HTMLNode Conversion Tests ===")
    
    # Test all TextType conversions
    test_nodes = [
        TextNode("Normal text", TextType.NORMAL),
        TextNode("Bold text", TextType.BOLD),
        TextNode("Italic text", TextType.ITALIC),
        TextNode("Code snippet", TextType.CODE),
        TextNode("Link text", TextType.LINK, "https://boot.dev"),
        TextNode("Image alt text", TextType.IMAGE, "https://example.com/image.jpg")
    ]
    
    print("Converting TextNodes to HTMLNodes:")
    for text_node in test_nodes:
        html_node = text_node_to_html_node(text_node)
        print(f"  {text_node}")
        print(f"  → {html_node}")
        print(f"  → HTML: {html_node.to_html()}")
        print()
    
    # Test complete pipeline integration
    print("=== Complete Pipeline Integration ===")
    
    # Simulate parsing a paragraph with mixed formatting
    paragraph_content = [
        TextNode("This paragraph has ", TextType.NORMAL),
        TextNode("bold text", TextType.BOLD),
        TextNode(" and ", TextType.NORMAL),
        TextNode("italic text", TextType.ITALIC),
        TextNode(" and even a ", TextType.NORMAL),
        TextNode("link to Boot.dev", TextType.LINK, "https://boot.dev"),
        TextNode("!", TextType.NORMAL)
    ]
    
    # Convert all TextNodes to HTMLNodes
    html_children = []
    for text_node in paragraph_content:
        html_node = text_node_to_html_node(text_node)
        html_children.append(html_node)
    
    # Create a paragraph containing all the converted nodes
    paragraph = ParentNode("p", html_children)
    
    print("Original TextNodes:")
    for node in paragraph_content:
        print(f"  {node}")
    
    print(f"\nFinal paragraph HTML:")
    print(paragraph.to_html())
    
    # Test more complex document structure
    print("\n=== Complex Document Structure ===")
    
    # Create a blog post structure
    article_content = [
        # Header section
        ParentNode("header", [
            LeafNode("h1", "My Amazing Blog Post"),
            ParentNode("p", [
                LeafNode(None, "Published on "),
                LeafNode("time", "January 15, 2024", {"datetime": "2024-01-15"}),
                LeafNode(None, " by "),
                LeafNode("strong", "John Doe")
            ])
        ]),
        
        # Main content
        ParentNode("section", [
            ParentNode("p", [
                text_node_to_html_node(TextNode("This is the ", TextType.NORMAL)),
                text_node_to_html_node(TextNode("first paragraph", TextType.BOLD)),
                text_node_to_html_node(TextNode(" with some ", TextType.NORMAL)),
                text_node_to_html_node(TextNode("inline code", TextType.CODE)),
                text_node_to_html_node(TextNode(".", TextType.NORMAL))
            ]),
            
            ParentNode("p", [
                text_node_to_html_node(TextNode("Check out ", TextType.NORMAL)),
                text_node_to_html_node(TextNode("this amazing course", TextType.LINK, "https://boot.dev")),
                text_node_to_html_node(TextNode(" for learning programming!", TextType.NORMAL))
            ])
        ])
    ]
    
    article = ParentNode("article", article_content, {"class": "blog-post"})
    
    print("Complete blog post HTML:")
    print(article.to_html())
    
    # Test error handling
    print("\n=== Error Handling Tests ===")
    
    try:
        invalid_link = TextNode("Link without URL", TextType.LINK, None)
        text_node_to_html_node(invalid_link)
    except ValueError as e:
        print(f"Expected error for link without URL: {e}")
    
    try:
        invalid_image = TextNode("Image without URL", TextType.IMAGE, None)
        text_node_to_html_node(invalid_image)
    except ValueError as e:
        print(f"Expected error for image without URL: {e}")
    
    print("\n=== All Systems Complete! ===")
    print("✅ TextNode system working")
    print("✅ HTMLNode foundation solid") 
    print("✅ LeafNode generating HTML elements")
    print("✅ ParentNode handling complex structures")
    print("✅ TextNode to HTMLNode conversion working")
    print("✅ Complete pipeline: TextNode → HTMLNode → HTML string")
    print("🚀 Ready for Markdown parsing and full static site generation!")

if __name__ == "__main__":
    main()


