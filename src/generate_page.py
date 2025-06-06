import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    """
    Generate a complete HTML page from markdown content and template.
    
    This function:
    1. Reads markdown content from source file
    2. Reads HTML template
    3. Converts markdown to HTML
    4. Extracts title from markdown
    5. Replaces template placeholders with content and title
    6. Writes complete HTML page to destination
    
    Args:
        from_path (str): Path to the markdown source file
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML page will be written
    """
    print(f"📄 Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Step 1: Read the markdown file
    print(f"📖 Reading markdown file: {from_path}")
    try:
        with open(from_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        print(f"✅ Successfully read {len(markdown_content)} characters from {from_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {from_path}")
    except Exception as e:
        raise Exception(f"Error reading markdown file {from_path}: {e}")
    
    # Step 2: Read the template file
    print(f"📑 Reading template file: {template_path}")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        print(f"✅ Successfully read template from {template_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except Exception as e:
        raise Exception(f"Error reading template file {template_path}: {e}")
    
    # Step 3: Convert markdown to HTML
    print(f"🔄 Converting markdown to HTML...")
    try:
        html_node = markdown_to_html_node(markdown_content)
        content_html = html_node.to_html()
        print(f"✅ Successfully converted markdown to HTML ({len(content_html)} characters)")
    except Exception as e:
        raise Exception(f"Error converting markdown to HTML: {e}")
    
    # Step 4: Extract title from markdown
    print(f"🏷️  Extracting title from markdown...")
    try:
        page_title = extract_title(markdown_content)
        print(f"✅ Extracted title: '{page_title}'")
    except Exception as e:
        raise Exception(f"Error extracting title from markdown: {e}")
    
    # Step 5: Replace placeholders in template
    print(f"🔧 Replacing template placeholders...")
    try:
        # Replace the placeholders with actual content
        full_html = template_content.replace("{{ Title }}", page_title)
        full_html = full_html.replace("{{ Content }}", content_html)
        print(f"✅ Template placeholders replaced successfully")
    except Exception as e:
        raise Exception(f"Error replacing template placeholders: {e}")
    
    # Step 6: Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        print(f"📁 Creating destination directory: {dest_dir}")
        try:
            os.makedirs(dest_dir, exist_ok=True)
            print(f"✅ Created directory: {dest_dir}")
        except Exception as e:
            raise Exception(f"Error creating destination directory {dest_dir}: {e}")
    
    # Step 7: Write the complete HTML page to destination
    print(f"💾 Writing HTML page to: {dest_path}")
    try:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✅ Successfully wrote {len(full_html)} characters to {dest_path}")
    except Exception as e:
        raise Exception(f"Error writing HTML file {dest_path}: {e}")
    
    print(f"🎉 Page generation completed successfully!")
    return dest_path


def read_file(file_path):
    """
    Utility function to read a file and return its contents.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Contents of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")


def write_file(file_path, content):
    """
    Utility function to write content to a file.
    
    Args:
        file_path (str): Path where the file will be written
        content (str): Content to write to the file
    """
    # Ensure directory exists
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise Exception(f"Error writing file {file_path}: {e}")
