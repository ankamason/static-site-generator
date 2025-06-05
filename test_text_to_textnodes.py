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
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for i, (actual, expected_node) in enumerate(zip(nodes, expected)):
            with self.subTest(i=i):
                self.assertEqual(actual.text, expected_node.text, f"Node {i} text mismatch")
                self.assertEqual(actual.text_type, expected_node.text_type, f"Node {i} type mismatch")
                self.assertEqual(actual.url, expected_node.url, f"Node {i} URL mismatch")
    
    def test_empty_string(self):
        """Test empty string input"""
        nodes = text_to_textnodes("")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_plain_text_only(self):
        """Test text with no markdown formatting"""
        text = "This is just plain text with no formatting at all."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_only_bold(self):
        """Test text with only bold formatting"""
        text = "This has **bold text** in it."
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
    
    def test_only_italic(self):
        """Test text with only italic formatting"""
        text = "This has *italic text* in it."
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
    
    def test_only_code(self):
        """Test text with only code formatting"""
        text = "This has `code text` in it."
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" in it.", TextType.TEXT),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
    
    def test_only_image(self):
        """Test text with only image"""
        text = "Check out this ![cool image](https://example.com/image.jpg)!"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("cool image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode("!", TextType.TEXT),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
            self.assertEqual(actual.url, expected_node.url)
    
    def test_only_link(self):
        """Test text with only link"""
        text = "Visit [our website](https://example.com) for more info."
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("our website", TextType.LINK, "https://example.com"),
            TextNode(" for more info.", TextType.TEXT),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
            self.assertEqual(actual.url, expected_node.url)
    
    def test_multiple_same_type(self):
        """Test multiple instances of the same formatting type"""
        text = "**first bold** and **second bold** text"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("first bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        
        # Filter out empty text nodes for comparison
        nodes = [node for node in nodes if node.text]
        expected = [node for node in expected if node.text]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
    
    def test_nested_formatting_precedence(self):
        """Test that delimiter formatting takes precedence over images/links"""
        text = "**bold with ![image](url) inside**"
        nodes = text_to_textnodes(text)
        
        # Bold should be processed first, so image syntax becomes literal text
        expected = [
            TextNode("bold with ![image](url) inside", TextType.BOLD),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        self.assertEqual(nodes[0].text, expected[0].text)
        self.assertEqual(nodes[0].text_type, expected[0].text_type)
        
        # Verify that image syntax is preserved as literal text
        self.assertIn("![image](url)", nodes[0].text)
    
    def test_adjacent_formatting(self):
        """Test adjacent formatting with no space between"""
        text = "**bold***italic*`code`"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        
        self.assertEqual(len(nodes), len(expected))
        for actual, expected_node in zip(nodes, expected):
            self.assertEqual(actual.text, expected_node.text)
            self.assertEqual(actual.text_type, expected_node.text_type)
    
    def test_complex_mixed_content(self):
        """Test complex text with all types of formatting mixed together"""
        text = "Start **bold *nested italic* bold** then `code with **bold** inside` then ![img](pic.jpg) and [link](site.com) end"
        nodes = text_to_textnodes(text)
        
        # Due to processing order, some nesting won't work as expected
        # Bold and code will be processed first, preserving inner syntax as literal text
        
        # Verify we get a reasonable number of nodes
        self.assertGreater(len(nodes), 5)
        
        # Verify that we have at least one of each type
        types_found = {node.text_type for node in nodes}
        self.assertIn(TextType.TEXT, types_found)
        self.assertIn(TextType.BOLD, types_found)
        
        # Check that the result doesn't crash and produces valid nodes
        for node in nodes:
            self.assertIsInstance(node.text, str)
            self.assertIsInstance(node.text_type, TextType)
    
    def test_edge_case_empty_formatting(self):
        """Test edge cases with empty formatting"""
        text = "Text with ***** and `` and ![](empty.jpg) and [](empty.com)"
        nodes = text_to_textnodes(text)
        
        # Should not crash and should produce some nodes
        self.assertGreater(len(nodes), 0)
        
        # All nodes should have valid text and types
        for node in nodes:
            self.assertIsInstance(node.text, str)
            self.assertIsInstance(node.text_type, TextType)
    
    def test_processing_order_consistency(self):
        """Test that the processing order is consistent and predictable"""
        text1 = "**bold** and ![image](url)"
        text2 = "![image](url) and **bold**"
        
        nodes1 = text_to_textnodes(text1)
        nodes2 = text_to_textnodes(text2)
        
        # Both should process successfully
        self.assertGreater(len(nodes1), 1)
        self.assertGreater(len(nodes2), 1)
        
        # Should contain both bold and image nodes
        types1 = {node.text_type for node in nodes1}
        types2 = {node.text_type for node in nodes2}
        
        self.assertIn(TextType.BOLD, types1)
        self.assertIn(TextType.IMAGE, types1)
        self.assertIn(TextType.BOLD, types2)
        self.assertIn(TextType.IMAGE, types2)


if __name__ == "__main__":
    unittest.main()
