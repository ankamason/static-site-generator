import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    """
    Recursively copy all files and directories from source to destination.
    
    This function:
    1. Cleans the destination directory (removes all existing content)
    2. Recreates the destination directory structure
    3. Copies all files and subdirectories recursively
    4. Logs each operation for debugging
    
    Args:
        source_dir_path (str): Path to the source directory
        dest_dir_path (str): Path to the destination directory
    """
    print(f"🚀 Starting copy operation: {source_dir_path} → {dest_dir_path}")
    
    # Step 1: Clean the destination directory
    if os.path.exists(dest_dir_path):
        print(f"🧹 Cleaning existing destination: {dest_dir_path}")
        shutil.rmtree(dest_dir_path)
        print(f"✅ Removed existing directory: {dest_dir_path}")
    
    # Step 2: Create the destination directory
    print(f"📁 Creating destination directory: {dest_dir_path}")
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Step 3: Check if source directory exists
    if not os.path.exists(source_dir_path):
        print(f"❌ Source directory does not exist: {source_dir_path}")
        return
    
    # Step 4: Start the recursive copying
    print(f"📋 Scanning source directory: {source_dir_path}")
    copy_directory_contents(source_dir_path, dest_dir_path)
    
    print(f"🎉 Copy operation completed successfully!")


def copy_directory_contents(source_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    This is where the actual recursion happens. For each item in the source:
    - If it's a file: copy it directly
    - If it's a directory: create it in destination and recurse into it
    
    Args:
        source_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Get all items in the source directory
    try:
        items = os.listdir(source_dir)
        print(f"📂 Processing directory: {source_dir} (found {len(items)} items)")
    except PermissionError:
        print(f"❌ Permission denied accessing: {source_dir}")
        return
    except FileNotFoundError:
        print(f"❌ Directory not found: {source_dir}")
        return
    
    # Process each item in the directory
    for item in items:
        source_item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_item_path):
            # It's a file - copy it
            print(f"📄 Copying file: {source_item_path} → {dest_item_path}")
            try:
                shutil.copy2(source_item_path, dest_item_path)
                print(f"✅ File copied successfully: {item}")
            except Exception as e:
                print(f"❌ Error copying file {item}: {e}")
                
        elif os.path.isdir(source_item_path):
            # It's a directory - create it and recurse
            print(f"📁 Creating subdirectory: {dest_item_path}")
            try:
                os.makedirs(dest_item_path, exist_ok=True)
                print(f"✅ Directory created: {item}")
                
                # RECURSION: Process the subdirectory
                print(f"🔄 Recursing into: {source_item_path}")
                copy_directory_contents(source_item_path, dest_item_path)
                
            except Exception as e:
                print(f"❌ Error creating directory {item}: {e}")
        else:
            # It's neither a file nor directory (symlink, etc.)
            print(f"⚠️  Skipping special item: {item}")


# Convenience function for the main script
def copy_static_to_public():
    """
    Copy the static directory to public directory.
    
    This is a convenience function that uses the standard paths
    for this static site generator project.
    """
    copy_files_recursive("static", "public")
