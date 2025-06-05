import unittest
import sys
import os

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from block_type import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    
    # HEADING TESTS
    def test_heading_h1(self):
        """Test H1 heading identification"""
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h2(self):
        """Test H2 heading identification"""
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_h6(self):
        """Test H6 heading identification"""
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_invalid_too_many_hashes(self):
        """Test that 7+ # characters don't make a heading"""
        block = "####### This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_no_space_after_hash(self):
        """Test that # without space is not a heading"""
        block = "#This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading_hash_in_middle(self):
        """Test that # in middle of line is not a heading"""
        block = "This # is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # CODE BLOCK TESTS
    def test_code_block_simple(self):
        """Test simple code block"""
        block = "```\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        block = "```python\nprint('hello')\nprint('world')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_multiline(self):
        """Test multi-line code block"""
        block = "```\nfunction hello() {\n  console.log('hello');\n}\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_only_start(self):
        """Test that only opening ``` is not a code block"""
        block = "```\nprint('hello')"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_code_block_only_end(self):
        """Test that only closing ``` is not a code block"""
        block = "print('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # QUOTE TESTS
    def test_quote_single_line(self):
        """Test single line quote"""
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_multi_line(self):
        """Test multi-line quote"""
        block = "> This is a quote\n> that spans multiple\n> lines"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_with_spaces_after(self):
        """Test quote with spaces after >"""
        block = "> This is a quote\n>  This has extra space\n> This is normal"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_missing_one_line(self):
        """Test that missing > on one line makes it not a quote"""
        block = "> This is a quote\nThis line is missing >\n> This has it"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_quote_empty_line(self):
        """Test quote with empty line starting with >"""
        block = "> This is a quote\n>\n> With empty line"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)
    
    # UNORDERED LIST TESTS
    def test_unordered_list_single_item(self):
        """Test single item unordered list"""
        block = "- Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        """Test multi-item unordered list"""
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_missing_space(self):
        """Test that - without space is not a list"""
        block = "-Item 1\n-Item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_unordered_list_missing_one_dash(self):
        """Test that missing - on one line makes it not a list"""
        block = "- Item 1\nItem 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # ORDERED LIST TESTS
    def test_ordered_list_single_item(self):
        """Test single item ordered list"""
        block = "1. Item 1"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        """Test multi-item ordered list"""
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_long(self):
        """Test longer ordered list"""
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_ordered_list_wrong_start_number(self):
        """Test that starting with number other than 1 is not ordered list"""
        block = "2. Item 1\n3. Item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_skipped_number(self):
        """Test that skipping a number makes it not ordered list"""
        block = "1. Item 1\n3. Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_missing_space(self):
        """Test that missing space after . makes it not ordered list"""
        block = "1.Item 1\n2.Item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_ordered_list_missing_period(self):
        """Test that missing period makes it not ordered list"""
        block = "1 Item 1\n2 Item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # PARAGRAPH TESTS
    def test_paragraph_simple(self):
        """Test simple paragraph"""
        block = "This is just a regular paragraph of text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_multi_line(self):
        """Test multi-line paragraph"""
        block = "This is a paragraph\nthat spans multiple lines\nwith no special formatting."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_with_inline_formatting(self):
        """Test paragraph with inline markdown"""
        block = "This paragraph has **bold** and *italic* text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_numbers_not_list(self):
        """Test that numbers in text don't make it a list"""
        block = "In 1. the beginning, there was 2. darkness."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_paragraph_hash_not_heading(self):
        """Test that # in text doesn't make it a heading"""
        block = "Use the hashtag #awesome in your posts."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    # EDGE CASES
    def test_empty_block(self):
        """Test empty block"""
        block = ""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_whitespace_only(self):
        """Test block with only whitespace"""
        block = "   "
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
