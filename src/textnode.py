from enum import Enum
from markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Unbalanced delimiter: '{delimiter}' in {node.text}")

        for index, part in enumerate(parts):
            if index % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        current_text = node.text
        for image_alt, image_url in matches:
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            current_text = sections[1]
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        current_text = node.text
        for link_text, link_url in matches:
            sections = current_text.split(f"[{link_text}]({link_url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes