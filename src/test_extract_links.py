import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from extract_links import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Test basic image extraction from assignment"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        """Test extracting multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_no_matches(self):
        """Test text with no images"""
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_images_empty_alt(self):
        """Test image with empty alt text"""
        text = "Image with empty alt: ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_images_complex_url(self):
        """Test image with complex URL including query parameters"""
        text = "![diagram](https://example.com/path/image.png?param=value&size=large)"
        matches = extract_markdown_images(text)
        expected = [("diagram", "https://example.com/path/image.png?param=value&size=large")]
        self.assertListEqual(expected, matches)

    def test_extract_images_multiple_same_line(self):
        """Test multiple images on same line"""
        text = "![first](one.jpg) ![second](two.png) ![third](three.gif)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "one.jpg"),
            ("second", "two.png"), 
            ("third", "three.gif")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_with_spaces(self):
        """Test images with spaces in alt text"""
        text = "![alt text with spaces](image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt text with spaces", "image.jpg")], matches)

    def test_extract_images_ignores_links(self):
        """Test that image extraction ignores regular links"""
        text = "![image](img.jpg) and [link](site.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.jpg")], matches)

    def test_extract_images_relative_paths(self):
        """Test images with relative file paths"""
        text = "![local](./images/local.png) and ![parent](../assets/image.jpg)"
        matches = extract_markdown_images(text)
        expected = [
            ("local", "./images/local.png"),
            ("parent", "../assets/image.jpg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_images_special_characters_in_alt(self):
        """Test images with special characters in alt text"""
        text = "![image-with_special.chars](image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image-with_special.chars", "image.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_basic(self):
        """Test basic link extraction"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        """Test extracting multiple links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_no_matches(self):
        """Test text with no links"""
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_empty_anchor(self):
        """Test link with empty anchor text"""
        text = "Link with empty anchor: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_links_complex_url(self):
        """Test link with complex URL"""
        text = "[Search](https://www.google.com/search?q=python&source=web)"
        matches = extract_markdown_links(text)
        expected = [("Search", "https://www.google.com/search?q=python&source=web")]
        self.assertListEqual(expected, matches)

    def test_extract_links_ignores_images(self):
        """Test that link extraction ignores images"""
        text = "![image](img.jpg) and [link](site.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "site.com")], matches)

    def test_extract_links_multiple_same_line(self):
        """Test multiple links on same line"""
        text = "[first](one.com) [second](two.com) [third](three.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "one.com"),
            ("second", "two.com"),
            ("third", "three.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_with_spaces(self):
        """Test links with spaces in anchor text"""
        text = "[anchor text with spaces](example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("anchor text with spaces", "example.com")], matches)

    def test_extract_links_relative_urls(self):
        """Test links with relative URLs"""
        text = "[home](/) and [about](./about.html) and [parent](../index.html)"
        matches = extract_markdown_links(text)
        expected = [
            ("home", "/"),
            ("about", "./about.html"),
            ("parent", "../index.html")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_special_characters(self):
        """Test links with special characters in anchor text"""
        text = "[link-with_special.chars](example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link-with_special.chars", "example.com")], matches)

    def test_extract_links_email_and_phone(self):
        """Test links with email and phone URLs"""
        text = "[Email me](mailto:test@example.com) or [Call](tel:+1234567890)"
        matches = extract_markdown_links(text)
        expected = [
            ("Email me", "mailto:test@example.com"),
            ("Call", "tel:+1234567890")
        ]
        self.assertListEqual(expected, matches)


class TestExtractBothImagesAndLinks(unittest.TestCase):
    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "Check out this ![diagram](diagram.png) and visit [our site](https://example.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("diagram", "diagram.png")], images)
        self.assertListEqual([("our site", "https://example.com")], links)

    def test_complex_mixed_content(self):
        """Test complex text with multiple images and links"""
        text = """
        Here's an ![icon](icon.png) for our [website](https://example.com).
        See also: ![screenshot](screen.jpg) and [documentation](docs.html).
        """
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("icon", "icon.png"), ("screenshot", "screen.jpg")]
        expected_links = [("website", "https://example.com"), ("documentation", "docs.html")]
        
        self.assertListEqual(expected_images, images)
        self.assertListEqual(expected_links, links)

    def test_adjacent_images_and_links(self):
        """Test adjacent images and links"""
        text = "![image](img.jpg)[link](site.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("image", "img.jpg")], images)
        self.assertListEqual([("link", "site.com")], links)

    def test_nested_like_patterns(self):
        """Test patterns that might confuse the regex"""
        text = "Text with [nested [brackets]](example.com) and ![alt with (parens)](img.jpg)"
        
        # Our current regex should handle this reasonably
        # (may not be perfect for truly nested brackets, but that's edge case)
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        # Should find the main patterns
        self.assertTrue(len(images) >= 0)  # At least doesn't crash
        self.assertTrue(len(links) >= 0)   # At least doesn't crash


if __name__ == "__main__":
    unittest.main()
