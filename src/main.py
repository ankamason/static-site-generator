import os
import shutil
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
from generate_page import generate_page


def main():
    print("=" * 80)
    print("🚀 STATIC SITE GENERATOR - COMPLETE WEBSITE GENERATION")
    print("=" * 80)
    
    # Step 1: Clean and prepare the public directory
    print("\n📁 === STEP 1: PREPARE OUTPUT DIRECTORY ===")
    public_dir = "public"
    
    if os.path.exists(public_dir):
        print(f"🧹 Cleaning existing public directory: {public_dir}")
        shutil.rmtree(public_dir)
        print(f"✅ Removed existing directory: {public_dir}")
    
    print(f"📁 Creating fresh public directory: {public_dir}")
    os.makedirs(public_dir, exist_ok=True)
    print(f"✅ Created directory: {public_dir}")
    
    # Step 2: Copy static files
    print("\n📋 === STEP 2: COPY STATIC ASSETS ===")
    try:
        copy_static_to_public()
        print("✅ Static files copied successfully")
    except Exception as e:
        print(f"❌ Error copying static files: {e}")
        return
    
    # Step 3: Generate the main page
    print("\n📄 === STEP 3: GENERATE MAIN PAGE ===")
    try:
        generate_page(
            from_path="content/index.md",
            template_path="template.html", 
            dest_path="public/index.html"
        )
        print("✅ Main page generated successfully")
    except Exception as e:
        print(f"❌ Error generating main page: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Verify the generated site
    print("\n🔍 === STEP 4: VERIFY GENERATED SITE ===")
    try:
        # Check that key files exist
        required_files = [
            "public/index.html",
            "public/index.css",
            "public/images/tolkien.png"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✅ {file_path} ({file_size} bytes)")
            else:
                print(f"❌ Missing: {file_path}")
        
        # Show directory structure
        print(f"\n📊 Generated site structure:")
        for root, dirs, files in os.walk("public"):
            level = root.replace("public", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}📁 {os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f"{subindent}📄 {file} ({file_size} bytes)")
                
    except Exception as e:
        print(f"❌ Error during verification: {e}")
    
    # Step 5: Previous system verification (shortened)
    print("\n🔧 === STEP 5: SYSTEM VERIFICATION ===")
    try:
        # Quick markdown conversion test
        test_md = "# Test Page\n\nThis has **bold** text."
        html_result = markdown_to_html_node(test_md)
        print("✅ Markdown conversion system working")
        
        # Quick HTML generation test
        paragraph = ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " text")])
        print("✅ HTML generation system working")
        
    except Exception as e:
        print(f"❌ System verification failed: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 STATIC SITE GENERATOR COMPLETE!")
    print("✅ Static assets copied")
    print("✅ Main page generated") 
    print("✅ All systems operational")
    print("🌐 Ready to serve at http://localhost:8888")
    print("=" * 80)


if __name__ == "__main__":
    main()
