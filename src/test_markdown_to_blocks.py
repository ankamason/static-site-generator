import unittest
import sys
import os

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test the example from the assignment"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_single_block(self):
        """Test markdown with only one block"""
        md = "This is a single paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no blank lines."])
    
    def test_empty_string(self):
        """Test empty markdown string"""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_only_whitespace(self):
        """Test markdown with only whitespace"""
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_multiple_blank_lines(self):
        """Test markdown with multiple consecutive blank lines"""
        md = """First paragraph


Second paragraph



Third paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph", "Third paragraph"])
    
    def test_leading_trailing_whitespace(self):
        """Test blocks with leading and trailing whitespace"""
        md = """   First paragraph with leading spaces   

    Second paragraph with indentation    

Third paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "First paragraph with leading spaces",
            "Second paragraph with indentation",
            "Third paragraph"
        ])
    
    def test_various_block_types(self):
        """Test different types of markdown blocks"""
        md = """# This is a heading

This is a paragraph with **bold** and *italic* text.

- This is a list item
- Another list item
- Third list item

## Another heading

> This is a blockquote
> that spans multiple lines

```
This is a code block
with multiple lines
```

1. Ordered list item
2. Second ordered item"""
        
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph with **bold** and *italic* text.",
            "- This is a list item\n- Another list item\n- Third list item",
            "## Another heading",
            "> This is a blockquote\n> that spans multiple lines",
            "```\nThis is a code block\nwith multiple lines\n```",
            "1. Ordered list item\n2. Second ordered item"
        ]
        
        self.assertEqual(len(blocks), len(expected_blocks))
        for i, (actual, expected) in enumerate(zip(blocks, expected_blocks)):
            with self.subTest(i=i):
                self.assertEqual(actual, expected, f"Block {i} mismatch")
    
    def test_newlines_within_blocks(self):
        """Test that newlines within blocks are preserved"""
        md = """Paragraph line 1
Paragraph line 2
Paragraph line 3

List item 1
List item 2"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "Paragraph line 1\nParagraph line 2\nParagraph line 3",
            "List item 1\nList item 2"
        ])
    
    def test_real_markdown_document(self):
        """Test with a realistic markdown document structure"""
        md = """# My Blog Post

This is the introduction paragraph. It has some **important** information.

## Section 1

Here's the first section with some content.

- Key point one
- Key point two
- Key point three

## Section 2

Another section with different content.

> "This is an inspiring quote that really makes you think."

And here's the conclusion paragraph."""
        
        blocks = markdown_to_blocks(md)
        
        # Verify we get the expected number of blocks
        self.assertEqual(len(blocks), 9)
        
        # Verify specific blocks
        self.assertEqual(blocks[0], "# My Blog Post")
        self.assertEqual(blocks[1], "This is the introduction paragraph. It has some **important** information.")
        self.assertEqual(blocks[2], "## Section 1")
        self.assertEqual(blocks[3], "Here's the first section with some content.")
        self.assertEqual(blocks[4], "- Key point one\n- Key point two\n- Key point three")
        self.assertEqual(blocks[5], "## Section 2")
        self.assertEqual(blocks[6], "Another section with different content.")
        self.assertEqual(blocks[7], "> \"This is an inspiring quote that really makes you think.\"")
        self.assertEqual(blocks[8], "And here's the conclusion paragraph.")


if __name__ == "__main__":
    unittest.main()
