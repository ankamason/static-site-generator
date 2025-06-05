import unittest
import sys
import os

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    
    def test_assignment_example(self):
        """Test the exact example from the assignment"""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            with self.subTest(i=i):
                self.assertEqual(actual.text, expected_node.text, f"Node {i} text mismatch")
                self.assertEqual(actual.text_type, expected_node.text_type, f"Node {i} type mismatch")
                self.assertEqual(actual.url, expected_node.url, f"Node {i} URL mismatch")
    
    def test_plain_text(self):
        """Test plain text with no formatting"""
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("This is just plain text", TextType.NORMAL)]
        self.assertEqual(nodes, expected)
    
    def test_only_bold(self):
        """Test text with only bold formatting"""
        text = "**bold text**"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("bold text", TextType.BOLD)]
        self.assertEqual(nodes, expected)
    
    def test_only_italic(self):
        """Test text with only italic formatting"""
        text = "*italic text*"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("italic text", TextType.ITALIC)]
        self.assertEqual(nodes, expected)
    
    def test_only_code(self):
        """Test text with only code formatting"""
        text = "`code text`"
        nodes = text_to_textnodes(text)
        
        expected = [TextNode("code text", TextType.CODE)]
        self.assertEqual(nodes, expected)
    
    def test_multiple_formatting(self):
        """Test text with multiple different formatting types"""
        text = "**bold** and *italic* and `code`"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
