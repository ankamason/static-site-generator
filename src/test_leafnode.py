import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """Test basic paragraph rendering"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        """Test link with href attribute"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        """Test raw text (no HTML tag)"""
        node = LeafNode(None, "Just some raw text")
        self.assertEqual(node.to_html(), "Just some raw text")

    def test_leaf_to_html_multiple_props(self):
        """Test element with multiple attributes"""
        node = LeafNode("a", "Link text", {
            "href": "https://www.boot.dev",
            "target": "_blank",
            "class": "external-link"
        })
        result = node.to_html()
        # Check that all attributes are present
        self.assertIn('href="https://www.boot.dev"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('class="external-link"', result)
        # Check structure
        self.assertTrue(result.startswith('<a '))
        self.assertTrue(result.endswith('>Link text</a>'))

    def test_leaf_to_html_empty_props(self):
        """Test element with empty props dictionary"""
        node = LeafNode("p", "Text content", {})
        self.assertEqual(node.to_html(), "<p>Text content</p>")

    def test_leaf_to_html_no_props(self):
        """Test element with no props (None)"""
        node = LeafNode("span", "Span content")
        self.assertEqual(node.to_html(), "<span>Span content</span>")

    def test_leaf_to_html_self_closing_style(self):
        """Test elements that are typically self-closing but have content"""
        # Note: LeafNode always generates opening and closing tags
        node = LeafNode("img", "alt text", {"src": "image.jpg", "alt": "An image"})
        expected = '<img src="image.jpg" alt="An image">alt text</img>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_special_characters(self):
        """Test content with special characters"""
        node = LeafNode("p", "Text with <special> characters & symbols")
        expected = "<p>Text with <special> characters & symbols</p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_raises_value_error(self):
        """Test that missing value raises ValueError"""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")

    def test_leaf_constructor_no_children(self):
        """Test that constructor properly sets children to None"""
        node = LeafNode("p", "Test content")
        self.assertIsNone(node.children)

    def test_leaf_constructor_inheritance(self):
        """Test that LeafNode properly inherits from HTMLNode"""
        node = LeafNode("div", "Content", {"class": "test"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.props, {"class": "test"})
        self.assertIsNone(node.children)

    def test_leaf_repr_inherited(self):
        """Test that LeafNode inherits __repr__ from HTMLNode"""
        node = LeafNode("p", "Test", {"id": "test"})
        expected = "HTMLNode(p, Test, children: None, {'id': 'test'})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
