import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        """Test props_to_html with multiple attributes"""
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_single_prop(self):
        """Test props_to_html with single attribute"""
        node = HTMLNode(tag="img", props={"src": "image.jpg"})
        expected = ' src="image.jpg"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        """Test props_to_html with no attributes"""
        node = HTMLNode(tag="p", value="Hello")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty_props(self):
        """Test props_to_html with empty dictionary"""
        node = HTMLNode(tag="div", props={})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        """Test that to_html raises NotImplementedError"""
        node = HTMLNode(tag="p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_with_all_attributes(self):
        """Test string representation with all attributes"""
        children = [HTMLNode(tag="span", value="child")]
        node = HTMLNode(
            tag="div",
            value="test",
            children=children,
            props={"class": "container"}
        )
        expected = "HTMLNode(div, test, children: [HTMLNode(span, child, children: None, None)], {'class': 'container'})"
        self.assertEqual(repr(node), expected)

    def test_repr_minimal(self):
        """Test string representation with minimal attributes"""
        node = HTMLNode()
        expected = "HTMLNode(None, None, children: None, None)"
        self.assertEqual(repr(node), expected)

    def test_init_default_values(self):
        """Test that constructor defaults work correctly"""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        """Test constructor with all values provided"""
        children = [HTMLNode(value="child")]
        props = {"id": "test"}
        node = HTMLNode(tag="div", value="content", children=children, props=props)
        
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_special_characters(self):
        """Test props_to_html with special characters in values"""
        node = HTMLNode(
            tag="a",
            props={"title": "This has \"quotes\" and 'apostrophes'"}
        )
        expected = ' title="This has "quotes" and \'apostrophes\'"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_maintains_order(self):
        """Test that props_to_html processes dictionary items"""
        # Note: Dictionary order is preserved in Python 3.7+
        node = HTMLNode(
            tag="input",
            props={"type": "text", "name": "username", "id": "user_input"}
        )
        result = node.props_to_html()
        # Check that all attributes are present
        self.assertIn('type="text"', result)
        self.assertIn('name="username"', result)
        self.assertIn('id="user_input"', result)
        # Check that it starts with a space
        self.assertTrue(result.startswith(' '))

    def test_children_list_structure(self):
        """Test that children can be a complex nested structure"""
        grandchild = HTMLNode(tag="strong", value="bold")
        child = HTMLNode(tag="span", children=[grandchild])
        parent = HTMLNode(tag="div", children=[child])
        
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[0].children[0].tag, "strong")
        self.assertEqual(parent.children[0].children[0].value, "bold")


if __name__ == "__main__":
    unittest.main()
