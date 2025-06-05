import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_single(self):
        """Test splitting single code block"""
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_bold_single(self):
        """Test splitting single bold text"""
        node = TextNode("This is **bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_italic_single(self):
        """Test splitting single italic text"""
        node = TextNode("This is *italic* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_multiple_same_delimiter(self):
        """Test splitting multiple instances of same delimiter"""
        node = TextNode("This is **bold** and **more bold** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_delimiter_at_start(self):
        """Test delimiter at start of text"""
        node = TextNode("**bold** at start", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_delimiter_at_end(self):
        """Test delimiter at end of text"""
        node = TextNode("Text ends with **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("Text ends with ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_delimiter_only(self):
        """Test text that is only delimited content"""
        node = TextNode("**only bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "only bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_no_delimiter(self):
        """Test text with no delimiters - should return unchanged"""
        node = TextNode("This text has no formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no formatting")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)

    def test_split_preserves_non_text_nodes(self):
        """Test that non-TEXT nodes are preserved unchanged"""
        nodes = [
            TextNode("Normal text with **bold**", TextType.NORMAL),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
            TextNode("More normal with **bold**", TextType.NORMAL),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        # Should have: split normal, unchanged bold, unchanged italic, split normal
        self.assertEqual(len(new_nodes), 6)
        
        # Check that non-TEXT nodes are preserved
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "Already italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)

    def test_split_empty_delimiter_content(self):
        """Test empty content between delimiters"""
        node = TextNode("Text with **** empty bold", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Should skip empty parts
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode(" empty bold", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 2)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_raises_error_unclosed_delimiter(self):
        """Test that unclosed delimiter raises ValueError"""
        node = TextNode("This has **unclosed bold text", TextType.NORMAL)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertIn("unclosed delimiter", str(context.exception))
        self.assertIn("**", str(context.exception))

    def test_split_raises_error_unclosed_at_start(self):
        """Test unclosed delimiter at start raises error"""
        node = TextNode("**unclosed at start", TextType.NORMAL)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_complex_multiple_delimiters(self):
        """Test complex text with multiple different patterns"""
        node = TextNode("Start **bold** middle `code` end **more bold**", TextType.NORMAL)
        
        # First pass: split bold
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_after_bold = [
            TextNode("Start ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" middle `code` end ", TextType.NORMAL),
            TextNode("more bold", TextType.BOLD),
        ]
        
        self.assertEqual(len(nodes), 4)
        for i, expected_node in enumerate(expected_after_bold):
            self.assertEqual(nodes[i].text, expected_node.text)
            self.assertEqual(nodes[i].text_type, expected_node.text_type)
        
        # Second pass: split code on the results
        final_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_final = [
            TextNode("Start ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),  # Unchanged
            TextNode(" middle ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" end ", TextType.NORMAL),
            TextNode("more bold", TextType.BOLD),  # Unchanged
        ]
        
        self.assertEqual(len(final_nodes), 6)
        for i, expected_node in enumerate(expected_final):
            self.assertEqual(final_nodes[i].text, expected_node.text)
            self.assertEqual(final_nodes[i].text_type, expected_node.text_type)

    def test_split_adjacent_delimiters(self):
        """Test adjacent delimiters"""
        node = TextNode("**first****second** text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode("second", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 3)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)

    def test_split_single_character_delimiter(self):
        """Test single character delimiters like backtick"""
        node = TextNode("Code `x` and `y` variables", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Code ", TextType.NORMAL),
            TextNode("x", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("y", TextType.CODE),
            TextNode(" variables", TextType.NORMAL),
        ]
        
        self.assertEqual(len(new_nodes), 5)
        for i, expected_node in enumerate(expected):
            self.assertEqual(new_nodes[i].text, expected_node.text)
            self.assertEqual(new_nodes[i].text_type, expected_node.text_type)


if __name__ == "__main__":
    unittest.main()
