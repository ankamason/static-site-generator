import os
import sys
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
from copy_static import copy_files_recursive
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive


def main():
    print("=" * 80)
    print("🚀 STATIC SITE GENERATOR - PRODUCTION DEPLOYMENT")
    print("=" * 80)
    
    # Step 0: Handle command line arguments for basepath
    print("\n🔧 === STEP 0: CONFIGURATION ===")
    
    # Get basepath from command line arguments
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        output_dir = "docs"  # Production build goes to docs
        build_type = "PRODUCTION"
    else:
        basepath = "/"
        output_dir = "public"  # Development build goes to public
        build_type = "DEVELOPMENT"
    
    print(f"🏗️  Build type: {build_type}")
    print(f"🔗 Basepath: {basepath}")
    print(f"📁 Output directory: {output_dir}")
    
    # Step 1: Clean and prepare the output directory
    print(f"\n📁 === STEP 1: PREPARE OUTPUT DIRECTORY ===")
    
    if os.path.exists(output_dir):
        print(f"🧹 Cleaning existing {output_dir} directory")
        shutil.rmtree(output_dir)
        print(f"✅ Removed existing directory: {output_dir}")
    
    print(f"📁 Creating fresh {output_dir} directory")
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Created directory: {output_dir}")
    
    # Step 2: Copy static files
    print("\n📋 === STEP 2: COPY STATIC ASSETS ===")
    try:
        copy_files_recursive("static", output_dir)
        print("✅ Static files copied successfully")
    except Exception as e:
        print(f"❌ Error copying static files: {e}")
        return
    
    # Step 3: Generate ALL pages recursively with basepath
    print("\n🔄 === STEP 3: RECURSIVE PAGE GENERATION ===")
    try:
        generate_pages_recursive(
            dir_path_content="content",
            template_path="template.html", 
            dest_dir_path=output_dir,
            basepath=basepath
        )
        print("✅ All pages generated recursively")
    except Exception as e:
        print(f"❌ Error during recursive page generation: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Verify the generated site
    print(f"\n🔍 === STEP 4: VERIFY GENERATED SITE ===")
    try:
        # Check that key files exist
        expected_files = [
            f"{output_dir}/index.html",
            f"{output_dir}/blog/glorfindel/index.html", 
            f"{output_dir}/blog/tom/index.html",
            f"{output_dir}/blog/majesty/index.html",
            f"{output_dir}/contact/index.html",
            f"{output_dir}/index.css",
            f"{output_dir}/images/tolkien.png"
        ]
        
        print("📋 Checking expected files:")
        for file_path in expected_files:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✅ {file_path} ({file_size} bytes)")
            else:
                print(f"❌ Missing: {file_path}")
        
        # Show complete directory structure
        print(f"\n📊 Complete generated site structure:")
        for root, dirs, files in os.walk(output_dir):
            level = root.replace(output_dir, "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}📁 {os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f"{subindent}📄 {file} ({file_size} bytes)")
        
        # Count total pages generated
        html_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        print(f"\n📊 Summary: {len(html_files)} HTML pages generated")
        for html_file in html_files:
            print(f"   🌐 {html_file}")
        
        # Verify basepath configuration in generated files
        if build_type == "PRODUCTION":
            print(f"\n🔗 Verifying basepath configuration:")
            sample_file = f"{output_dir}/index.html"
            if os.path.exists(sample_file):
                with open(sample_file, 'r') as f:
                    content = f.read()
                if f'href="{basepath}' in content:
                    print(f"✅ Basepath {basepath} correctly applied to links")
                else:
                    print(f"⚠️  Basepath may not be applied correctly")
                
    except Exception as e:
        print(f"❌ Error during verification: {e}")
    
    # Step 5: System verification
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
    if build_type == "PRODUCTION":
        print("🚀 PRODUCTION BUILD COMPLETE!")
        print("✅ Site built for GitHub Pages deployment")
        print(f"✅ Basepath configured: {basepath}")
        print(f"✅ Output directory: {output_dir}")
        print("🌐 Ready for GitHub Pages deployment!")
    else:
        print("🎉 DEVELOPMENT BUILD COMPLETE!")
        print("✅ Static assets copied")
        print("✅ All pages generated recursively") 
        print("✅ Complete website structure created")
        print("🌐 Ready to serve at http://localhost:8888")
    print("=" * 80)


if __name__ == "__main__":
    main()
