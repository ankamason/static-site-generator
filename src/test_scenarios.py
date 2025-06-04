"""
Scenario tests for HTMLNode - these test how HTMLNode will be used
in practice for generating static site content.
"""
import unittest
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from htmlnode import HTMLNode


class TestHTMLNodeScenarios(unittest.TestCase):
    def test_blog_post_structure(self):
        """Test creating a blog post structure with HTMLNodes"""
        # Create a blog post: <article><h1>Title</h1><p>Content with <a>link</a></p></article>
        link = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://boot.dev"})
        paragraph_content = [
            HTMLNode(value="Read more at "),
            link,
            HTMLNode(value=" for great courses!")
        ]
        paragraph = HTMLNode(tag="p", children=paragraph_content)
        heading = HTMLNode(tag="h1", value="My Blog Post")
        article = HTMLNode(tag="article", children=[heading, paragraph])
        
        # Verify structure
        self.assertEqual(article.tag, "article")
        self.assertEqual(len(article.children), 2)
        self.assertEqual(article.children[0].value, "My Blog Post")
        self.assertEqual(article.children[1].children[1].props["href"], "https://boot.dev")

    def test_navigation_menu(self):
        """Test creating a navigation menu structure"""
        # Create <nav><ul><li><a>Home</a></li><li><a>About</a></li></ul></nav>
        home_link = HTMLNode(tag="a", value="Home", props={"href": "/"})
        about_link = HTMLNode(tag="a", value="About", props={"href": "/about"})
        
        home_item = HTMLNode(tag="li", children=[home_link])
        about_item = HTMLNode(tag="li", children=[about_link])
        
        nav_list = HTMLNode(tag="ul", children=[home_item, about_item])
        nav = HTMLNode(tag="nav", children=[nav_list])
        
        # Verify navigation structure
        self.assertEqual(nav.tag, "nav")
        self.assertEqual(nav.children[0].tag, "ul")
        self.assertEqual(len(nav.children[0].children), 2)
        
        # Check first menu item
        first_item = nav.children[0].children[0]
        self.assertEqual(first_item.tag, "li")
        self.assertEqual(first_item.children[0].value, "Home")
        self.assertEqual(first_item.children[0].props["href"], "/")

    def test_image_with_caption(self):
        """Test creating a figure with image and caption"""
        # Create <figure><img src="photo.jpg" alt="A photo"><figcaption>My Photo</figcaption></figure>
        img = HTMLNode(
            tag="img", 
            props={"src": "photo.jpg", "alt": "A photo"}
        )
        caption = HTMLNode(tag="figcaption", value="My Photo")
        figure = HTMLNode(tag="figure", children=[img, caption])
        
        # Verify structure
        self.assertEqual(figure.tag, "figure")
        self.assertEqual(len(figure.children), 2)
        self.assertEqual(figure.children[0].props["src"], "photo.jpg")
        self.assertEqual(figure.children[1].value, "My Photo")


if __name__ == "__main__":
    unittest.main()
