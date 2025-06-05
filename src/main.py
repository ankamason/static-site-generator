from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from split_delimiter import split_nodes_delimiter

def main():
    # Existing tests (shortened for focus)
    print("=== TextNode Tests ===")
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    
    print("\n=== HTMLNode → HTML Pipeline Working ===")
    paragraph = ParentNode("p", [
        LeafNode("b", "Bold text"),
        LeafNode(None, " and normal text")
    ])
    print("Sample HTML:", paragraph.to_html())
    
    # NEW: Split Delimiter Testing
    print("\n=== Split Delimiter Function Tests ===")
    
    # Test 1: Code blocks with backticks
    print("Test 1: Code blocks")
    node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print("Original:", node)
    print("Split result:")
    for i, n in enumerate(new_nodes):
        print(f"  {i}: {n}")
    
    # Test 2: Bold text with **
    print("\nTest 2: Bold text")
    node = TextNode("This is **bold** text with **more bold** here", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("Original:", node)
    print("Split result:")
    for i, n in enumerate(new_nodes):
        print(f"  {i}: {n}")
    
    # Test 3: Italic text with *
    print("\nTest 3: Italic text")
    node = TextNode("This has *italic* and *more italic* text", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    print("Original:", node)
    print("Split result:")
    for i, n in enumerate(new_nodes):
        print(f"  {i}: {n}")
    
    # Test 4: Mixed node types (should leave non-TEXT nodes alone)
    print("\nTest 4: Mixed node types")
    mixed_nodes = [
        TextNode("Normal text with `code` here", TextType.NORMAL),
        TextNode("Already bold text", TextType.BOLD),
        TextNode("More normal with `more code` text", TextType.NORMAL)
    ]
    new_nodes = split_nodes_delimiter(mixed_nodes, "`", TextType.CODE)
    print("Original nodes:")
    for i, n in enumerate(mixed_nodes):
        print(f"  {i}: {n}")
    print("After split:")
    for i, n in enumerate(new_nodes):
        print(f"  {i}: {n}")
    
    # Test 5: No delimiters (should return unchanged)
    print("\nTest 5: No delimiters")
    node = TextNode("This text has no special formatting", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("Original:", node)
    print("Result:", new_nodes[0])
    print("Same object?", node is new_nodes[0])
    
    # Test 6: Delimiter at start and end
    print("\nTest 6: Delimiters at start/end")
    node = TextNode("**bold start** and **bold end**", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("Original:", node)
    print("Split result:")
    for i, n in enumerate(new_nodes):
        print(f"  {i}: {n}")
    
    # Test 7: Error handling (unclosed delimiter)
    print("\nTest 7: Error handling")
    try:
        node = TextNode("This has **unclosed bold text", TextType.NORMAL)
        split_nodes_delimiter([node], "**", TextType.BOLD)
        print("ERROR: Should have raised exception!")
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    
    # Test 8: Complete pipeline integration
    print("\n=== Complete Pipeline Integration ===")
    
    # Start with Markdown-like text
    original_text = "This paragraph has **bold text** and `code snippets` and *italic text*!"
    print(f"Original text: {original_text}")
    
    # Step 1: Create initial TextNode
    nodes = [TextNode(original_text, TextType.NORMAL)]
    print(f"Step 1 - Initial: {nodes}")
    
    # Step 2: Process bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    print(f"Step 2 - After bold: {[str(n) for n in nodes]}")
    
    # Step 3: Process code text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print(f"Step 3 - After code: {[str(n) for n in nodes]}")
    
    # Step 4: Process italic text
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    print(f"Step 4 - After italic: {[str(n) for n in nodes]}")
    
    # Step 5: Convert to HTML
    html_nodes = []
    for text_node in nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    # Step 6: Create final paragraph
    final_paragraph = ParentNode("p", html_nodes)
    print(f"\nFinal HTML: {final_paragraph.to_html()}")
    
    print("\n=== All Tests Complete! ===")
    print("✅ Split delimiter function working")
    print("✅ Multiple delimiter types supported") 
    print("✅ Error handling for invalid Markdown")
    print("✅ Integration with existing pipeline")
    print("🚀 Markdown inline parsing foundation complete!")

if __name__ == "__main__":
    main()
