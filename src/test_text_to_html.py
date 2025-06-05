import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        """Test normal text conversion"""
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_bold(self):
        """Test bold text conversion"""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_italic(self):
        """Test italic text conversion"""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_code(self):
        """Test code text conversion"""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)
        self.assertIsNone(html_node.children)

    def test_link(self):
        """Test link conversion"""
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertIsNone(html_node.children)

    def test_image(self):
        """Test image conversion"""
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://example.com/image.jpg",
            "alt": "Alt text"
        })
        self.assertIsNone(html_node.children)

    def test_to_html_output(self):
        """Test that converted nodes generate correct HTML"""
        # Test normal text
        text_node = TextNode("Plain text", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Plain text")
        
        # Test bold
        bold_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
        
        # Test italic
        italic_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(italic_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
        
        # Test code
        code_node = TextNode("console.log('hi')", TextType.CODE)
        html_node = text_node_to_html_node(code_node)
        self.assertEqual(html_node.to_html(), "<code>console.log('hi')</code>")
        
        # Test link
        link_node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(link_node)
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')
        
        # Test image
        img_node = TextNode("A cool image", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(img_node)
        expected = '<img src="image.png" alt="A cool image"></img>'
        self.assertEqual(html_node.to_html(), expected)

    def test_link_without_url_raises_error(self):
        """Test that link without URL raises ValueError"""
        node = TextNode("Link text", TextType.LINK, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link nodes must have a URL")

    def test_image_without_url_raises_error(self):
        """Test that image without URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image nodes must have a URL")

    def test_unknown_text_type_raises_error(self):
        """Test that unknown TextType raises ValueError"""
        # Create a mock TextNode with invalid type
        node = TextNode("Test", TextType.NORMAL)
        node.text_type = "INVALID_TYPE"  # Manually set invalid type
        
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unknown TextType", str(context.exception))

    def test_empty_text_handling(self):
        """Test conversion with empty text content"""
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b></b>")

    def test_special_characters_in_text(self):
        """Test that special characters are preserved"""
        special_text = "Text with <special> & characters"
        node = TextNode(special_text, TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, special_text)
        self.assertEqual(html_node.to_html(), special_text)

    def test_url_with_special_characters(self):
        """Test URLs with query parameters and special characters"""
        url = "https://example.com/page?param=value&other=test"
        node = TextNode("Link", TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["href"], url)


if __name__ == "__main__":
    unittest.main()
