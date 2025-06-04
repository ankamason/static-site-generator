from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    # Test TextNode (existing)
    print("=== TextNode Tests ===")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
    # Test HTMLNode
    print("\n=== HTMLNode Tests ===")
    
    # Test with props
    html_node = HTMLNode(
        tag="a",
        value="Click me!",
        props={"href": "https://www.google.com", "target": "_blank"}
    )
    print("HTML Node with props:")
    print(html_node)
    print("Props to HTML:", repr(html_node.props_to_html()))
    
    # Test with children
    child1 = HTMLNode(tag="b", value="Bold text")
    child2 = HTMLNode(value=" and some normal text")
    parent = HTMLNode(tag="p", children=[child1, child2])
    print("\nHTML Node with children:")
    print(parent)
    
    # Test with no props
    simple_node = HTMLNode(tag="h1", value="Hello World")
    print("\nSimple HTML Node:")
    print(simple_node)
    print("Props to HTML:", repr(simple_node.props_to_html()))

if __name__ == "__main__":
    main()
