import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        """Test basic parent with one child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test nested parent nodes (recursion)"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        """Test parent with multiple child nodes"""
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "Italic text")
        parent = ParentNode("p", [child1, child2, child3])
        expected = "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_props(self):
        """Test parent node with HTML attributes"""
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        result = parent.to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn("<span>content</span>", result)
        self.assertTrue(result.startswith("<div"))
        self.assertTrue(result.endswith("</div>"))

    def test_to_html_no_props(self):
        """Test parent node without attributes"""
        child = LeafNode("p", "paragraph")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p>paragraph</p></div>")

    def test_to_html_complex_nesting(self):
        """Test deeply nested structure with multiple levels"""
        # Create: <article><section><div><p><b>text</b></p></div></section></article>
        deep_child = LeafNode("b", "deeply nested text")
        level3 = ParentNode("p", [deep_child])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        root = ParentNode("article", [level1])
        
        expected = "<article><section><div><p><b>deeply nested text</b></p></div></section></article>"
        self.assertEqual(root.to_html(), expected)

    def test_to_html_mixed_children_types(self):
        """Test parent containing both LeafNodes and ParentNodes"""
        leaf1 = LeafNode(None, "Start text ")
        nested_parent = ParentNode("strong", [LeafNode(None, "bold content")])
        leaf2 = LeafNode(None, " end text")
        
        parent = ParentNode("p", [leaf1, nested_parent, leaf2])
        expected = "<p>Start text <strong>bold content</strong> end text</p>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_list_structure(self):
        """Test creating HTML list structure"""
        item1 = ParentNode("li", [LeafNode(None, "First item")])
        item2 = ParentNode("li", [LeafNode(None, "Second item")])
        item3 = ParentNode("li", [
            LeafNode(None, "Third item with "),
            LeafNode("a", "link", {"href": "https://example.com"})
        ])
        
        ul = ParentNode("ul", [item1, item2, item3])
        result = ul.to_html()
        
        self.assertIn("<ul>", result)
        self.assertIn("</ul>", result)
        self.assertIn("<li>First item</li>", result)
        self.assertIn("<li>Second item</li>", result)
        self.assertIn('<li>Third item with <a href="https://example.com">link</a></li>', result)

    def test_to_html_table_structure(self):
        """Test creating complex table structure"""
        header_cell1 = ParentNode("th", [LeafNode(None, "Name")])
        header_cell2 = ParentNode("th", [LeafNode(None, "Age")])
        header_row = ParentNode("tr", [header_cell1, header_cell2])
        
        data_cell1 = ParentNode("td", [LeafNode(None, "John")])
        data_cell2 = ParentNode("td", [LeafNode(None, "25")])
        data_row = ParentNode("tr", [data_cell1, data_cell2])
        
        table = ParentNode("table", [header_row, data_row])
        expected = "<table><tr><th>Name</th><th>Age</th></tr><tr><td>John</td><td>25</td></tr></table>"
        self.assertEqual(table.to_html(), expected)

    def test_to_html_raises_error_no_tag(self):
        """Test that missing tag raises ValueError"""
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_to_html_raises_error_no_children(self):
        """Test that None children raises ValueError"""
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children")

    def test_to_html_raises_error_empty_children(self):
        """Test that empty children list raises ValueError"""
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children")

    def test_constructor_sets_value_to_none(self):
        """Test that constructor properly sets value to None"""
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child])
        self.assertIsNone(parent.value)

    def test_constructor_inheritance(self):
        """Test that ParentNode properly inherits from HTMLNode"""
        child = LeafNode("p", "content")
        parent = ParentNode("div", [child], {"class": "test"})
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"class": "test"})
        self.assertIsNone(parent.value)

    def test_repr_inherited(self):
        """Test that ParentNode inherits __repr__ from HTMLNode"""
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child], {"id": "container"})
        result = repr(parent)
        
        self.assertIn("HTMLNode(div,", result)
        self.assertIn("None,", result)  # value should be None
        self.assertIn("children:", result)
        self.assertIn("{'id': 'container'}", result)

    def test_props_to_html_inherited(self):
        """Test that ParentNode uses inherited props_to_html method"""
        child = LeafNode("span", "content")
        parent = ParentNode("div", [child], {
            "class": "container",
            "data-test": "value"
        })
        
        props_html = parent.props_to_html()
        self.assertIn('class="container"', props_html)
        self.assertIn('data-test="value"', props_html)
        self.assertTrue(props_html.startswith(' '))

    def test_recursive_depth_stress_test(self):
        """Test handling of deeply nested structures"""
        # Create a 5-level deep nesting
        current = LeafNode("span", "bottom level")
        
        for i in range(5):
            current = ParentNode("div", [current], {"level": str(i)})
        
        result = current.to_html()
        
        # Should have 5 opening div tags
        self.assertEqual(result.count("<div"), 5)
        self.assertEqual(result.count("</div>"), 5)
        self.assertIn("<span>bottom level</span>", result)


if __name__ == "__main__":
    unittest.main()
