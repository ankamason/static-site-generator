import unittest
import sys
import os

# Add the src directory to Python path for relative imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test the paragraph example from the assignment"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        """Test the code block example from the assignment"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_single_paragraph(self):
        """Test single paragraph conversion"""
        md = "This is a simple paragraph with **bold** text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a simple paragraph with <b>bold</b> text.</p></div>"
        )
    
    def test_headings(self):
        """Test different heading levels"""
        md = """# Heading 1

## Heading 2

### Heading 3 with **bold**

#### Heading 4

##### Heading 5

###### Heading 6"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block(self):
        """Test quote block conversion"""
        md = """> This is a quote
> with multiple lines
> and **bold** text"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote\nwith multiple lines\nand <b>bold</b> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        """Test unordered list conversion"""
        md = """- First item with **bold**
- Second item with *italic*
- Third item with `code`"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        md = """1. First item
2. Second item with **bold**
3. Third item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        md = """```python
def hello():
    print("Hello, world!")
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><pre><code>def hello():\n    print(\"Hello, world!\")\n</code></pre></div>"
        self.assertEqual(html, expected)
    
    def test_mixed_content(self):
        """Test document with all block types"""
        md = """# Main Heading

This is a paragraph with **bold** and *italic* text.

## Subheading

Here's a quote:

> Life is what happens
> when you're busy making other plans

Some code:

```
function greet(name) {
    return "Hello, " + name;
}
```

A list of features:

- **Bold** text support
- *Italic* text support  
- `Code` inline support

And an ordered list:

1. First step
2. Second step
3. Final step"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Verify it contains all the expected elements
        self.assertIn("<h1>Main Heading</h1>", html)
        self.assertIn("<h2>Subheading</h2>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<blockquote>Life is what happens\nwhen you're busy making other plans</blockquote>", html)
        self.assertIn("<pre><code>function greet(name) {\n    return \"Hello, \" + name;\n}\n</code></pre>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<ol>", html)
        self.assertIn("<li><b>Bold</b> text support</li>", html)
        
        # Verify overall structure
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
    
    def test_empty_markdown(self):
        """Test empty markdown document"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p></p></div>")
    
    def test_whitespace_only(self):
        """Test markdown with only whitespace"""
        md = "\n\n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p></p></div>")
    
    def test_inline_markdown_in_headings(self):
        """Test that inline markdown works in headings"""
        md = "# Heading with **bold** and *italic*"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading with <b>bold</b> and <i>italic</i></h1></div>"
        self.assertEqual(html, expected)
    
    def test_links_and_images(self):
        """Test that links and images work in paragraphs"""
        md = """This paragraph has a [link](https://example.com) and an ![image](image.jpg)."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This paragraph has a <a href="https://example.com">link</a> and an <img src="image.jpg" alt="image"></img>.</p></div>'
        self.assertEqual(html, expected)
    
    def test_complex_nested_formatting(self):
        """Test complex nested inline formatting"""
        md = """This has **bold with *italic inside* and `code`** text."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # The exact result depends on your processing order, but it should contain the text
        self.assertIn("This has", html)
        self.assertIn("text.", html)
        self.assertTrue(html.startswith("<div><p>"))
        self.assertTrue(html.endswith("</p></div>"))


if __name__ == "__main__":
    unittest.main()
