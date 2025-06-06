import unittest
import sys
import os
import tempfile
import shutil

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from copy_static import copy_files_recursive


class TestCopyStatic(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures with temporary directories"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        
        # Create source directory structure
        os.makedirs(self.source_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_copy_single_file(self):
        """Test copying a single file"""
        # Create a test file
        test_file = os.path.join(self.source_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        
        # Copy the directory
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Verify the file was copied
        dest_file = os.path.join(self.dest_dir, "test.txt")
        self.assertTrue(os.path.exists(dest_file))
        
        with open(dest_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "test content")
    
    def test_copy_nested_directories(self):
        """Test copying nested directory structure"""
        # Create nested structure
        nested_dir = os.path.join(self.source_dir, "subdir", "nested")
        os.makedirs(nested_dir)
        
        # Create files at different levels
        with open(os.path.join(self.source_dir, "root.txt"), "w") as f:
            f.write("root file")
        
        with open(os.path.join(self.source_dir, "subdir", "sub.txt"), "w") as f:
            f.write("sub file")
            
        with open(os.path.join(nested_dir, "nested.txt"), "w") as f:
            f.write("nested file")
        
        # Copy the directory
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Verify all files were copied
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "root.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "subdir", "sub.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "subdir", "nested", "nested.txt")))
    
    def test_clean_destination(self):
        """Test that destination is cleaned before copying"""
        # Create destination with existing content
        os.makedirs(self.dest_dir)
        old_file = os.path.join(self.dest_dir, "old.txt")
        with open(old_file, "w") as f:
            f.write("old content")
        
        # Create source with new content
        new_file = os.path.join(self.source_dir, "new.txt")
        with open(new_file, "w") as f:
            f.write("new content")
        
        # Copy
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Verify old file is gone, new file exists
        self.assertFalse(os.path.exists(old_file))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "new.txt")))
    
    def test_empty_source_directory(self):
        """Test copying from empty source directory"""
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Destination should exist but be empty
        self.assertTrue(os.path.exists(self.dest_dir))
        self.assertEqual(len(os.listdir(self.dest_dir)), 0)


if __name__ == "__main__":
    unittest.main()
