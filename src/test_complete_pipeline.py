import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter
from split_images_links import split_nodes_image, split_nodes_link
from text_to_html import text_node_to_html_node
from parentnode import ParentNode


class TestCompletePipeline(unittest.TestCase):
    def test_complete_markdown_to_html_pipeline(self):
        """Test the complete pipeline from Markdown text to HTML"""
        # Start with complex Markdown text
        markdown_text = "This has **bold** and ![image](img.jpg) and [link](site.com) and `code`!"
        
        # Step 1: Create initial TextNode
        nodes = [TextNode(markdown_text, TextType.NORMAL)]
        
        # Step 2: Process all delimiter types
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # Step 3: Process images and links
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        
        # Step 4: Verify we have the expected TextNodes
        expected_nodes = [
            TextNode("This has ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "site.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode("!", TextType.NORMAL),
        ]
        
        self.assertEqual(len(nodes), len(expected_nodes))
        for i, (actual, expected) in enumerate(zip(nodes, expected_nodes)):
            self.assertEqual(actual.text, expected.text, f"Node {i} text mismatch")
            self.assertEqual(actual.text_type, expected.text_type, f"Node {i} type mismatch") 
            self.assertEqual(actual.url, expected.url, f"Node {i} URL mismatch")
        
        # Step 5: Convert to HTMLNodes
        html_nodes = []
        for text_node in nodes:
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(html_node)
        
        # Step 6: Create final HTML paragraph
        paragraph = ParentNode("p", html_nodes)
        final_html = paragraph.to_html()
        
        # Step 7: Verify final HTML output
        expected_html = '<p>This has <b>bold</b> and <img src="img.jpg" alt="image"></img> and <a href="site.com">link</a> and <code>code</code>!</p>'
        self.assertEqual(final_html, expected_html)

    def test_complex_nested_markdown(self):
        """Test complex Markdown with multiple formatting types - demonstrates processing order"""
        markdown_text = "Check out this **bold ![image](pic.jpg) with link [here](url.com)** and `code`!"
        
        # Process through complete pipeline
        nodes = [TextNode(markdown_text, TextType.NORMAL)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        
        # Convert to HTML
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        paragraph = ParentNode("p", html_nodes)
        final_html = paragraph.to_html()
        
        # IMPORTANT: Due to processing order, bold is processed FIRST,
        # so the image and link syntax is trapped inside the bold TextNode
        # and will NOT be converted to actual images/links.
        # This is the correct behavior - bold delimiters take precedence.
        
        expected_html = '<p>Check out this <b>bold ![image](pic.jpg) with link [here](url.com)</b> and <code>code</code>!</p>'
        self.assertEqual(final_html, expected_html)
        
        # Verify that bold and code formatting worked
        self.assertIn("<b>", final_html)
        self.assertIn("<code>", final_html)
        
        # The image and link syntax should remain as literal text inside the bold
        self.assertIn("![image](pic.jpg)", final_html)
        self.assertIn("[here](url.com)", final_html)

    def test_non_nested_formatting_works(self):
        """Test that non-nested formatting processes correctly"""
        markdown_text = "**bold** then ![image](pic.jpg) then [link](url.com) then `code`"
        
        # Process through complete pipeline
        nodes = [TextNode(markdown_text, TextType.NORMAL)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        
        # Convert to HTML
        html_nodes = [text_node_to_html_node(node) for node in nodes]
        paragraph = ParentNode("p", html_nodes)
        final_html = paragraph.to_html()
        
        # When NOT nested, all formatting should work
        self.assertIn("<b>bold</b>", final_html)
        self.assertIn('<img src="pic.jpg"', final_html)
        self.assertIn('<a href="url.com"', final_html)
        self.assertIn("<code>code</code>", final_html)

    def test_order_independence(self):
        """Test that processing order doesn't affect final result for non-overlapping formats"""
        markdown_text = "Text with **bold** and ![img](url) and [link](site) here"
        
        # Process in one order
        nodes1 = [TextNode(markdown_text, TextType.NORMAL)]
        nodes1 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)
        nodes1 = split_nodes_image(nodes1)
        nodes1 = split_nodes_link(nodes1)
        
        # Process in different order
        nodes2 = [TextNode(markdown_text, TextType.NORMAL)]
        nodes2 = split_nodes_image(nodes2)
        nodes2 = split_nodes_link(nodes2)
        nodes2 = split_nodes_delimiter(nodes2, "**", TextType.BOLD)
        
        # Convert both to HTML
        html1 = ParentNode("p", [text_node_to_html_node(n) for n in nodes1]).to_html()
        html2 = ParentNode("p", [text_node_to_html_node(n) for n in nodes2]).to_html()
        
        # Should produce same final HTML when not nested
        self.assertEqual(html1, html2)

    def test_empty_and_edge_cases(self):
        """Test edge cases throughout the pipeline"""
        test_cases = [
            "",  # Empty string
            "Just plain text",  # No formatting
            "**bold**",  # Only formatting
            "![](empty-alt.jpg)",  # Empty alt text
            "[](empty-anchor.com)",  # Empty anchor text
        ]
        
        for text in test_cases:
            with self.subTest(text=text):
                nodes = [TextNode(text, TextType.NORMAL)]
                nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
                nodes = split_nodes_image(nodes)
                nodes = split_nodes_link(nodes)
                
                # Should not crash and should produce valid HTML
                html_nodes = [text_node_to_html_node(n) for n in nodes if n.text]
                if html_nodes:
                    paragraph = ParentNode("p", html_nodes)
                    html = paragraph.to_html()
                    self.assertIsInstance(html, str)
                    self.assertTrue(html.startswith("<p>"))
                    self.assertTrue(html.endswith("</p>"))

    def test_processing_order_explanation(self):
        """Test that demonstrates why processing order matters"""
        # Test case 1: Bold processed first (current behavior)
        text1 = "**bold with ![image](url) inside**"
        nodes1 = [TextNode(text1, TextType.NORMAL)]
        nodes1 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)  # First
        nodes1 = split_nodes_image(nodes1)  # Second
        
        # The bold text "bold with ![image](url) inside" is now a BOLD TextNode
        # split_nodes_image only processes NORMAL nodes, so image syntax is preserved as text
        html1 = ParentNode("p", [text_node_to_html_node(n) for n in nodes1]).to_html()
        self.assertIn("![image](url)", html1)  # Image syntax preserved as text
        self.assertNotIn("<img", html1)  # No actual image tag
        
        # Test case 2: Images processed first - this creates broken bold syntax
        text2 = "**bold with ![image](url) inside**"
        nodes2 = [TextNode(text2, TextType.NORMAL)]
        nodes2 = split_nodes_image(nodes2)  # First - this breaks the bold delimiters
        
        # After image processing, we have nodes like:
        # ["**bold with ", TextNode("image", IMAGE, "url"), " inside**"]
        # Now when we try to process bold, we get unmatched delimiters
        
        # We expect this to either:
        # 1. Leave unmatched delimiters as literal text, OR
        # 2. Handle gracefully without crashing
        
        # Let's test that it doesn't crash and handles gracefully
        try:
            nodes2 = split_nodes_delimiter(nodes2, "**", TextType.BOLD)  # Second
            html2 = ParentNode("p", [text_node_to_html_node(n) for n in nodes2]).to_html()
            
            # The results should be different, showing order matters for nested syntax
            self.assertNotEqual(html1, html2)
            
            # In this case, the bold delimiters should be treated as literal text
            # since they're now unmatched after image processing
            self.assertIn("**", html2)  # Literal ** should remain
            self.assertIn('<img src="url"', html2)  # Image should be processed
            
        except ValueError as e:
            # If your implementation throws an error for unmatched delimiters,
            # that's also acceptable behavior - it shows the processing order issue
            self.assertIn("unclosed delimiter", str(e))
            print(f"Expected error for unmatched delimiters: {e}")


if __name__ == "__main__":
    unittest.main()
