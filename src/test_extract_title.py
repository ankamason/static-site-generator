import unittest
import sys
import os

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    
    def test_extract_title_simple(self):
        """Test extracting a simple title"""
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_extract_title_with_content(self):
        """Test extracting title from markdown with additional content"""
        markdown = """# My Title

This is some content below the title.

## Subheading

More content here."""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_extract_title_with_whitespace(self):
        """Test extracting title with leading/trailing whitespace"""
        markdown = "#   Spaced Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "Spaced Title")
    
    def test_extract_title_with_leading_whitespace(self):
        """Test extracting title from line with leading whitespace"""
        markdown = "   # Indented Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Indented Title")
    
    def test_extract_title_multiline_with_empty_lines(self):
        """Test extracting title when there are empty lines before it"""
        markdown = """

# Title After Empty Lines

Content here."""
        result = extract_title(markdown)
        self.assertEqual(result, "Title After Empty Lines")
    
    def test_extract_title_ignores_h2_and_below(self):
        """Test that h2, h3, etc. headers are ignored when looking for h1"""
        markdown = """## This is h2

### This is h3

# This is h1

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "This is h1")
    
    def test_extract_title_first_h1_only(self):
        """Test that only the first h1 is returned"""
        markdown = """# First Title

Some content

# Second Title

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")
    
    def test_extract_title_with_special_characters(self):
        """Test extracting title with special characters"""
        markdown = "# Title with **bold** and *italic* and `code`"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with **bold** and *italic* and `code`")
    
    def test_extract_title_with_numbers_and_symbols(self):
        """Test extracting title with numbers and symbols"""
        markdown = "# Chapter 1: The Beginning (Part 1)"
        result = extract_title(markdown)
        self.assertEqual(result, "Chapter 1: The Beginning (Part 1)")
    
    def test_no_h1_header_raises_exception(self):
        """Test that missing h1 header raises ValueError"""
        markdown = """## Only h2 here

### And h3

Some content but no h1."""
        
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_empty_markdown_raises_exception(self):
        """Test that empty markdown raises ValueError"""
        with self.assertRaises(ValueError) as context:
            extract_title("")
        
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_whitespace_only_raises_exception(self):
        """Test that whitespace-only markdown raises ValueError"""
        with self.assertRaises(ValueError) as context:
            extract_title("   \n\n   ")
        
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_hash_without_space_not_h1(self):
        """Test that # without space is not considered h1"""
        markdown = """#NotATitle

## This is h2

Some content."""
        
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_empty_h1_raises_exception(self):
        """Test that h1 with no content raises ValueError"""
        markdown = "# "
        
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_h1_with_only_whitespace_raises_exception(self):
        """Test that h1 with only whitespace raises ValueError"""
        markdown = "#   \n\nSome content"
        
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        
        self.assertIn("No h1 header found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
