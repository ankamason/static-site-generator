from textnode import TextNode, TextType

def main():
    # Test with a link node
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
    # Test with normal text
    node2 = TextNode("Just regular text", TextType.NORMAL)
    print(node2)
    
    # Test equality
    node3 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(f"node == node3: {node == node3}")

if __name__ == "__main__":
    main()
