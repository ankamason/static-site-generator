"""
Real-world scenario tests for LeafNode - demonstrating how LeafNode
will be used to generate actual web page content.
"""
import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from leafnode import LeafNode


class TestLeafNodeScenarios(unittest.TestCase):
    def test_blog_content_elements(self):
        """Test creating typical blog content elements"""
        # Blog post title
        title = LeafNode("h1", "My Amazing Blog Post")
        self.assertEqual(title.to_html(), "<h1>My Amazing Blog Post</h1>")
        
        # External link
        external_link = LeafNode("a", "Visit Boot.dev", {
            "href": "https://boot.dev",
            "target": "_blank",
            "rel": "noopener"
        })
        result = external_link.to_html()
        self.assertIn('href="https://boot.dev"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn("Visit Boot.dev", result)
        
        # Code snippet
        code = LeafNode("code", "print('Hello, World!')")
        self.assertEqual(code.to_html(), "<code>print('Hello, World!')</code>")
        
        # Emphasized text
        emphasis = LeafNode("em", "This is really important!")
        self.assertEqual(emphasis.to_html(), "<em>This is really important!</em>")

    def test_navigation_elements(self):
        """Test creating navigation menu elements"""
        # Home link
        home = LeafNode("a", "Home", {"href": "/", "class": "nav-link"})
        expected = '<a href="/" class="nav-link">Home</a>'
        self.assertEqual(home.to_html(), expected)
        
        # Current page (no link, just text)
        current = LeafNode("span", "About", {"class": "nav-current"})
        expected = '<span class="nav-current">About</span>'
        self.assertEqual(current.to_html(), expected)

    def test_form_elements(self):
        """Test creating form-related elements"""
        # Submit button
        submit = LeafNode("button", "Submit Form", {
            "type": "submit",
            "class": "btn btn-primary"
        })
        result = submit.to_html()
        self.assertIn('type="submit"', result)
        self.assertIn('class="btn btn-primary"', result)
        self.assertIn("Submit Form", result)
        
        # Label
        label = LeafNode("label", "Email Address:", {"for": "email"})
        expected = '<label for="email">Email Address:</label>'
        self.assertEqual(label.to_html(), expected)

    def test_semantic_html_elements(self):
        """Test creating semantic HTML5 elements"""
        # Article heading
        heading = LeafNode("h2", "Section Title")
        self.assertEqual(heading.to_html(), "<h2>Section Title</h2>")
        
        # Time element
        time_elem = LeafNode("time", "2024-01-15", {"datetime": "2024-01-15"})
        expected = '<time datetime="2024-01-15">2024-01-15</time>'
        self.assertEqual(time_elem.to_html(), expected)
        
        # Mark (highlighted text)
        mark = LeafNode("mark", "highlighted text")
        self.assertEqual(mark.to_html(), "<mark>highlighted text</mark>")

    def test_mixed_content_preparation(self):
        """Test LeafNodes that will be used within paragraph content"""
        # These would typically be children of a ParentNode paragraph
        plain_text = LeafNode(None, "This is some ")
        bold_text = LeafNode("strong", "important")
        more_text = LeafNode(None, " information with a ")
        link = LeafNode("a", "helpful link", {"href": "https://example.com"})
        end_text = LeafNode(None, ".")
        
        # Test individual pieces
        self.assertEqual(plain_text.to_html(), "This is some ")
        self.assertEqual(bold_text.to_html(), "<strong>important</strong>")
        self.assertEqual(more_text.to_html(), " information with a ")
        self.assertEqual(link.to_html(), '<a href="https://example.com">helpful link</a>')
        self.assertEqual(end_text.to_html(), ".")
        
        # These would combine to create:
        # "This is some <strong>important</strong> information with a <a href="...">helpful link</a>."


if __name__ == "__main__":
    unittest.main()
