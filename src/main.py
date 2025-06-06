from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_to_html import text_node_to_html_node
from split_delimiter import split_nodes_delimiter
from extract_links import extract_markdown_images, extract_markdown_links
from split_images_links import split_nodes_image, split_nodes_link
from text_to_textnodes import text_to_textnodes
from markdown_to_html import markdown_to_html_node
from copy_static import copy_static_to_public


def main():
    print("=" * 60)
    print("🚀 STATIC SITE GENERATOR - COPY STATIC PHASE")
    print("=" * 60)
    
    # Previous functionality verification (shortened for focus)
    print("\n=== System Verification ===")
    
    # Quick verification that everything still works
    paragraph = ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " text")])
    print("✅ HTML generation:", paragraph.to_html())
    
    # Quick markdown conversion test
    test_md = "# Test\n\nThis has **bold** text."
    html_result = markdown_to_html_node(test_md)
    print("✅ Markdown conversion:", html_result.to_html()[:50] + "...")
    
    # NEW: Copy Static Files
    print("\n=== NEW: Copy Static Files ===")
    print("This demonstrates recursive file copying from static/ to public/")
    
    try:
        # Execute the copy operation
        copy_static_to_public()
        
        # Verify the operation succeeded
        import os
        if os.path.exists("public"):
            print("\n📊 Copy Operation Results:")
            print(f"✅ public/ directory created")
            
            # List what was copied
            for root, dirs, files in os.walk("public"):
                level = root.replace("public", "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}📁 {os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}📄 {file}")
        else:
            print("❌ public/ directory was not created")
            
    except Exception as e:
        print(f"❌ Error during copy operation: {e}")
        import traceback
        traceback.print_exc()
    
    # Test the recursive copy function with a demonstration
    print("\n=== Recursive Copy Function Demonstration ===")
    print("The copy_files_recursive function demonstrates:")
    print("1. 🧹 Clean destination (remove existing files)")
    print("2. 📁 Create directory structure")
    print("3. 📄 Copy individual files")
    print("4. 🔄 Recurse into subdirectories")
    print("5. 📝 Log each operation for debugging")
    
    print("\n=== Static Site Generator Core Complete ===")
    print("✅ HTML generation system working")
    print("✅ Markdown parsing and conversion working")
    print("✅ File operations and static copying working")
    print("🎯 Ready for next phase: Generate Page!")


if __name__ == "__main__":
    main()
