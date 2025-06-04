import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """Test basic equality with same text and type"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        """Test equality when both nodes have URLs"""
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_with_url_none(self):
        """Test that explicit None equals default None"""
        node = TextNode("Just text", TextType.NORMAL, None)
        node2 = TextNode("Just text", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        """Test inequality when text content differs"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        """Test inequality when text types differ"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        """Test inequality when URLs differ"""
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        """Test inequality when one has URL and other doesn't"""
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_repr_with_url(self):
        """Test string representation with URL"""
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        expected = "TextNode(Click here, link, https://www.boot.dev)"
        self.assertEqual(repr(node), expected)

    def test_repr_without_url(self):
        """Test string representation without URL"""
        node = TextNode("Bold text", TextType.BOLD)
        expected = "TextNode(Bold text, bold, None)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
