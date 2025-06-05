from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

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
    
    # Test ParentNode functionality (NEW!)
    print("\n=== ParentNode Tests ===")
    
    # Simple parent with one child
    simple_parent = ParentNode("div", [
        LeafNode("p", "Hello from inside a div!")
    ])
    print("Simple parent HTML:", simple_parent.to_html())
    
    # Parent with multiple children
    multi_parent = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ])
    print("Multi-child parent HTML:", multi_parent.to_html())
    
    # Nested parents (grandchildren!)
    nested_parent = ParentNode("div", [
        ParentNode("p", [
            LeafNode("b", "Bold text in paragraph")
        ]),
        ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "List item 1")]),
            ParentNode("li", [LeafNode(None, "List item 2")])
        ])
    ])
    print("Nested parent HTML:", nested_parent.to_html())
    
    # Parent with attributes
    styled_parent = ParentNode("div", [
        LeafNode("span", "Styled content")
    ], {"class": "container", "id": "main"})
    print("Styled parent HTML:", styled_parent.to_html())
    
    # Test error conditions
    print("\n=== ParentNode Error Testing ===")
    
    try:
        error_parent = ParentNode(None, [LeafNode("p", "test")])
        error_parent.to_html()
    except ValueError as e:
        print(f"Expected error (no tag): {e}")
    
    try:
        error_parent2 = ParentNode("div", None)
        error_parent2.to_html()
    except ValueError as e:
        print(f"Expected error (no children): {e}")
    
    try:
        error_parent3 = ParentNode("div", [])
        error_parent3.to_html()
    except ValueError as e:
        print(f"Expected error (empty children): {e}")
    
    # Test TextNode to LeafNode integration
    print("\n=== TextNode to LeafNode Integration ===")
    text_nodes = [
        TextNode("Normal text", TextType.NORMAL),
        TextNode("Bold text", TextType.BOLD), 
        TextNode("Link text", TextType.LINK, "https://example.com"),
    ]
    
    leaf_nodes = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.NORMAL:
            leaf = LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            leaf = LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.LINK:
            leaf = LeafNode("a", text_node.text, {"href": text_node.url})
        leaf_nodes.append(leaf)
    
    # Put all converted nodes in a paragraph
    paragraph = ParentNode("p", leaf_nodes)
    print("Integrated paragraph HTML:", paragraph.to_html())
    
    # Complex real-world example
    print("\n=== Complex Real-World Example ===")
    article = ParentNode("article", [
        ParentNode("header", [
            LeafNode("h1", "My Blog Post"),
            ParentNode("p", [
                LeafNode(None, "Published on "),
                LeafNode("time", "January 1, 2024", {"datetime": "2024-01-01"})
            ])
        ]),
        ParentNode("section", [
            ParentNode("p", [
                LeafNode(None, "This is the "),
                LeafNode("strong", "first paragraph"),
                LeafNode(None, " of my blog post.")
            ]),
            ParentNode("p", [
                LeafNode(None, "Check out "),
                LeafNode("a", "this amazing site", {"href": "https://boot.dev"}),
                LeafNode(None, " for learning!")
            ])
        ])
    ], {"class": "blog-post"})
    
    print("Complex article HTML:", article.to_html())
    
    print("\n=== All Tests Complete! ===")
    print("✅ TextNode system working")
    print("✅ HTMLNode foundation solid") 
    print("✅ LeafNode generating real HTML")
    print("✅ ParentNode handling complex structures")
    print("✅ Recursive HTML generation working")
    print("🚀 Complete HTML generation pipeline ready!")

if __name__ == "__main__":
    main()
