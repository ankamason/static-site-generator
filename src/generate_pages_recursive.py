import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages for all markdown files in a directory structure.
    
    This function crawls through every directory and subdirectory in the content path,
    finds all .md files, and generates corresponding .html files in the destination
    directory with the same structure.
    
    Args:
        dir_path_content (str): Root directory containing markdown content files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Root directory where HTML files will be generated
        
    Example:
        content/blog/post/index.md → public/blog/post/index.html
        content/about/index.md → public/about/index.html
    """
    print(f"🔄 Starting recursive page generation:")
    print(f"   📁 Content directory: {dir_path_content}")
    print(f"   📝 Template: {template_path}")
    print(f"   🎯 Destination: {dest_dir_path}")
    print()
    
    # Verify the content directory exists
    if not os.path.exists(dir_path_content):
        print(f"❌ Content directory does not exist: {dir_path_content}")
        return
    
    if not os.path.isdir(dir_path_content):
        print(f"❌ Content path is not a directory: {dir_path_content}")
        return
    
    # Start the recursive processing
    total_pages = _process_directory_recursive(dir_path_content, template_path, dest_dir_path, dir_path_content)
    
    print(f"\n🎉 Recursive generation completed!")
    print(f"📊 Total pages generated: {total_pages}")


def _process_directory_recursive(current_dir, template_path, dest_base_dir, content_base_dir):
    """
    Helper function that recursively processes a directory and all its subdirectories.
    
    This is where the actual recursion happens. For each directory:
    1. Process all .md files in the current directory
    2. For each subdirectory, recursively call this function
    
    Args:
        current_dir (str): Current directory being processed
        template_path (str): Path to the HTML template
        dest_base_dir (str): Base destination directory
        content_base_dir (str): Base content directory (for calculating relative paths)
        
    Returns:
        int: Number of pages generated in this directory and all subdirectories
    """
    pages_generated = 0
    
    try:
        # Get all items in the current directory
        items = os.listdir(current_dir)
        print(f"📂 Processing directory: {current_dir}")
        print(f"   Found {len(items)} items")
        
    except PermissionError:
        print(f"❌ Permission denied accessing: {current_dir}")
        return 0
    except Exception as e:
        print(f"❌ Error accessing directory {current_dir}: {e}")
        return 0
    
    # Process each item in the directory
    for item in items:
        item_path = os.path.join(current_dir, item)
        
        if os.path.isfile(item_path):
            # It's a file - check if it's a markdown file
            if item.endswith('.md'):
                print(f"📄 Found markdown file: {item}")
                
                # Calculate the corresponding output path
                # Remove the base content directory from the path to get relative path
                relative_path = os.path.relpath(item_path, content_base_dir)
                
                # Change .md extension to .html
                relative_html_path = relative_path[:-3] + '.html'  # Remove .md, add .html
                
                # Create full destination path
                dest_file_path = os.path.join(dest_base_dir, relative_html_path)
                
                print(f"   📝 Generating: {relative_path} → {relative_html_path}")
                
                try:
                    # Generate the page
                    generate_page(item_path, template_path, dest_file_path)
                    pages_generated += 1
                    print(f"   ✅ Successfully generated: {dest_file_path}")
                    
                except Exception as e:
                    print(f"   ❌ Error generating page from {item_path}: {e}")
            else:
                print(f"📄 Skipping non-markdown file: {item}")
                
        elif os.path.isdir(item_path):
            # It's a directory - recurse into it
            print(f"📁 Found subdirectory: {item}")
            print(f"   🔄 Recursing into: {item_path}")
            
            # RECURSION: Process the subdirectory
            subdirectory_pages = _process_directory_recursive(
                item_path, 
                template_path, 
                dest_base_dir, 
                content_base_dir
            )
            
            pages_generated += subdirectory_pages
            print(f"   📊 Subdirectory {item} generated {subdirectory_pages} pages")
            
        else:
            print(f"⚠️  Skipping special item: {item}")
    
    print(f"✅ Completed directory {current_dir}: {pages_generated} pages generated")
    return pages_generated


def generate_all_pages(content_dir="content", template_path="template.html", dest_dir="public"):
    """
    Convenience function that generates all pages with standard paths.
    
    Args:
        content_dir (str): Content directory path (default: "content")
        template_path (str): Template file path (default: "template.html")
        dest_dir (str): Destination directory path (default: "public")
    """
    generate_pages_recursive(content_dir, template_path, dest_dir)
