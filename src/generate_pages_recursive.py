import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages for all markdown files in a directory structure.
    
    Args:
        dir_path_content (str): Root directory containing markdown content files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Root directory where HTML files will be generated
        basepath (str): Base URL path for the site (default: "/")
    """
    print(f"🔄 Starting recursive page generation:")
    print(f"   📁 Content directory: {dir_path_content}")
    print(f"   📝 Template: {template_path}")
    print(f"   🎯 Destination: {dest_dir_path}")
    print(f"   🔗 Basepath: {basepath}")
    print()
    
    # Verify the content directory exists
    if not os.path.exists(dir_path_content):
        print(f"❌ Content directory does not exist: {dir_path_content}")
        return
    
    if not os.path.isdir(dir_path_content):
        print(f"❌ Content path is not a directory: {dir_path_content}")
        return
    
    # Start the recursive processing
    total_pages = _process_directory_recursive(dir_path_content, template_path, dest_dir_path, dir_path_content, basepath)
    
    print(f"\n🎉 Recursive generation completed!")
    print(f"📊 Total pages generated: {total_pages}")


def _process_directory_recursive(current_dir, template_path, dest_base_dir, content_base_dir, basepath):
    """
    Helper function that recursively processes a directory and all its subdirectories.
    """
    pages_generated = 0
    
    try:
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
                relative_path = os.path.relpath(item_path, content_base_dir)
                relative_html_path = relative_path[:-3] + '.html'  # Remove .md, add .html
                dest_file_path = os.path.join(dest_base_dir, relative_html_path)
                
                print(f"   📝 Generating: {relative_path} → {relative_html_path}")
                
                try:
                    # Generate the page with basepath
                    generate_page(item_path, template_path, dest_file_path, basepath)
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
                content_base_dir,
                basepath
            )
            
            pages_generated += subdirectory_pages
            print(f"   📊 Subdirectory {item} generated {subdirectory_pages} pages")
            
        else:
            print(f"⚠️  Skipping special item: {item}")
    
    print(f"✅ Completed directory {current_dir}: {pages_generated} pages generated")
    return pages_generated

