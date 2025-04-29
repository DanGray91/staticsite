import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url_none(self):
        node1 = TextNode("Sample text", TextType.BOLD)
        node2 = TextNode("Sample text", TextType.BOLD)
        self.assertEqual(node1, node2)
    def test_different_texttype(self):
        node1 = TextNode("Sample text", TextType.BOLD)
        node2 = TextNode("Sample text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
if __name__ == "__main__":
    unittest.main()
