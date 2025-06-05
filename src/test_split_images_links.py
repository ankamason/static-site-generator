import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from textnode import TextNode, TextType
from split_images_links import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        """Test basic image splitting from assignment"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_single(self):
        """Test splitting single image"""
        node = TextNode("Text with ![single](image.jpg) here", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("single", TextType.IMAGE, "image.jpg"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_start(self):
        """Test image at start of text"""
        node = TextNode("![start](start.jpg) text after", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "start.jpg"),
            TextNode(" text after", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_at_end(self):
        """Test image at end of text"""
        node = TextNode("Text before ![end](end.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.NORMAL),
            TextNode("end", TextType.IMAGE, "end.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_only(self):
        """Test text that is only an image"""
        node = TextNode("![only](only.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only", TextType.IMAGE, "only.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_adjacent(self):
        """Test adjacent images with no text between"""
        node = TextNode("![first](first.jpg)![second](second.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "first.jpg"),
            TextNode("second", TextType.IMAGE, "second.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_images(self):
        """Test text with no images - should return original"""
        node = TextNode("Just plain text with no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_empty_alt(self):
        """Test image with empty alt text"""
        node = TextNode("Image with ![](empty-alt.jpg) here", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with ", TextType.NORMAL),
            TextNode("", TextType.IMAGE, "empty-alt.jpg"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_complex_url(self):
        """Test image with complex URL"""
        node = TextNode(
            "![diagram](https://example.com/path/image.png?param=value&size=large)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("diagram", TextType.IMAGE, "https://example.com/path/image.png?param=value&size=large"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_preserves_non_normal(self):
        """Test that non-NORMAL nodes are preserved unchanged"""
        nodes = [
            TextNode("Normal with ![image](img.jpg)", TextType.NORMAL),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        
        # Expected result:
        # [0] TextNode("Normal with ", TextType.NORMAL)     - from split of first node
        # [1] TextNode("image", TextType.IMAGE, "img.jpg")  - from split of first node  
        # [2] TextNode("Already bold", TextType.BOLD)       - preserved from original[1]
        # [3] TextNode("Already italic", TextType.ITALIC)   - preserved from original[2]
        
        self.assertEqual(len(new_nodes), 4)
        # Check the preserved bold node (now at index 2)
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Already bold")
        # Check the preserved italic node (now at index 3)
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[3].text, "Already italic")

    def test_split_images_multiple_same_alt(self):
        """Test multiple images with same alt text"""
        node = TextNode("![test](img1.jpg) and ![test](img2.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("test", TextType.IMAGE, "img1.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("test", TextType.IMAGE, "img2.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_special_characters(self):
        """Test images with special characters in alt text"""
        node = TextNode("![alt-with_special.chars](image.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("alt-with_special.chars", TextType.IMAGE, "image.png"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_basic(self):
        """Test basic link splitting"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_single(self):
        """Test splitting single link"""
        node = TextNode("Text with [single](link.com) here", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("single", TextType.LINK, "link.com"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_start(self):
        """Test link at start of text"""
        node = TextNode("[start](start.com) text after", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "start.com"),
            TextNode(" text after", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_at_end(self):
        """Test link at end of text"""
        node = TextNode("Text before [end](end.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.NORMAL),
            TextNode("end", TextType.LINK, "end.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_only(self):
        """Test text that is only a link"""
        node = TextNode("[only](only.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only", TextType.LINK, "only.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_adjacent(self):
        """Test adjacent links with no text between"""
        node = TextNode("[first](first.com)[second](second.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "first.com"),
            TextNode("second", TextType.LINK, "second.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        """Test text with no links - should return original"""
        node = TextNode("Just plain text with no links", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_empty_anchor(self):
        """Test link with empty anchor text"""
        node = TextNode("Link with [](empty-anchor.com) here", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with ", TextType.NORMAL),
            TextNode("", TextType.LINK, "empty-anchor.com"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_complex_url(self):
        """Test link with complex URL"""
        node = TextNode(
            "[Search](https://www.google.com/search?q=python&source=web)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Search", TextType.LINK, "https://www.google.com/search?q=python&source=web"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_preserves_non_normal(self):
        """Test that non-NORMAL nodes are preserved unchanged"""
        nodes = [
            TextNode("Normal with [link](url.com)", TextType.NORMAL),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already code", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        
        # Expected result:
        # [0] TextNode("Normal with ", TextType.NORMAL)     - from split of first node
        # [1] TextNode("link", TextType.LINK, "url.com")    - from split of first node  
        # [2] TextNode("Already bold", TextType.BOLD)       - preserved from original[1]
        # [3] TextNode("Already code", TextType.CODE)       - preserved from original[2]
        
        self.assertEqual(len(new_nodes), 4)
        # Check the preserved bold node (now at index 2)
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Already bold")
        # Check the preserved code node (now at index 3)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "Already code")

    def test_split_links_ignores_images(self):
        """Test that link splitting ignores image syntax"""
        node = TextNode("![image](img.jpg) and [link](site.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("![image](img.jpg) and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "site.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_special_characters(self):
        """Test links with special characters in anchor text"""
        node = TextNode("[anchor-with_special.chars](example.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("anchor-with_special.chars", TextType.LINK, "example.com"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitBothImagesAndLinks(unittest.TestCase):
    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        node = TextNode(
            "Text with ![image](img.jpg) and [link](site.com) here",
            TextType.NORMAL
        )
        
        # First split images
        after_images = split_nodes_image([node])
        expected_after_images = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and [link](site.com) here", TextType.NORMAL),
        ]
        self.assertListEqual(expected_after_images, after_images)
        
        # Then split links
        final_nodes = split_nodes_link(after_images)
        expected_final = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "site.com"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected_final, final_nodes)

    def test_complex_mixed_content(self):
        """Test complex text with multiple images and links"""
        node = TextNode(
            "Start ![img1](url1) middle [link1](site1) more ![img2](url2) end [link2](site2)",
            TextType.NORMAL
        )
        
        # Process images first, then links
        nodes_after_images = split_nodes_image([node])
        final_nodes = split_nodes_link(nodes_after_images)
        
        expected_final = [
            TextNode("Start ", TextType.NORMAL),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "site1"),
            TextNode(" more ", TextType.NORMAL),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "site2"),
        ]
        self.assertListEqual(expected_final, final_nodes)

    def test_adjacent_images_and_links(self):
        """Test adjacent images and links"""
        node = TextNode("![img](img.jpg)[link](site.com)", TextType.NORMAL)
        
        after_images = split_nodes_image([node])
        final_nodes = split_nodes_link(after_images)
        
        expected = [
            TextNode("img", TextType.IMAGE, "img.jpg"),
            TextNode("link", TextType.LINK, "site.com"),
        ]
        self.assertListEqual(expected, final_nodes)

    def test_empty_text_handling(self):
        """Test that empty text nodes are not added"""
        node = TextNode("![img](img.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        
        # Should only have the image node, no empty text nodes
        expected = [
            TextNode("img", TextType.IMAGE, "img.jpg"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_integration_with_delimiters(self):
        """Test that split functions work with delimiter-processed nodes"""
        # Simulate nodes that have been processed by split_nodes_delimiter
        nodes = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ![image](img.jpg) here", TextType.NORMAL),
        ]
        
        # Split images - should only affect the NORMAL nodes
        after_images = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),  # Unchanged
            TextNode(" and ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertListEqual(expected, after_images)

    def test_reverse_order_processing(self):
        """Test processing links first, then images"""
        node = TextNode(
            "![image](img.jpg) and [link](site.com)",
            TextType.NORMAL
        )
        
        # Process links first
        after_links = split_nodes_link([node])
        expected_after_links = [
            TextNode("![image](img.jpg) and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "site.com"),
        ]
        self.assertListEqual(expected_after_links, after_links)
        
        # Then process images
        final_nodes = split_nodes_image(after_links)
        expected_final = [
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "site.com"),
        ]
        self.assertListEqual(expected_final, final_nodes)

    def test_multiple_mixed_patterns(self):
        """Test multiple mixed patterns in complex arrangement"""
        node = TextNode(
            "![a](1) [b](2) ![c](3) [d](4) ![e](5)",
            TextType.NORMAL
        )
        
        # Process images first
        after_images = split_nodes_image([node])
        # Process links
        final_nodes = split_nodes_link(after_images)
        
        expected = [
            TextNode("a", TextType.IMAGE, "1"),
            TextNode(" ", TextType.NORMAL),
            TextNode("b", TextType.LINK, "2"),
            TextNode(" ", TextType.NORMAL),
            TextNode("c", TextType.IMAGE, "3"),
            TextNode(" ", TextType.NORMAL),
            TextNode("d", TextType.LINK, "4"),
            TextNode(" ", TextType.NORMAL),
            TextNode("e", TextType.IMAGE, "5"),
        ]
        self.assertListEqual(expected, final_nodes)


if __name__ == "__main__":
    unittest.main()
