from markdown import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children)

def text_to_children(text):
    """Convert text with inline markdown to a list of HTMLNode objects"""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode"""
    return ParentNode("p", text_to_children(block))

def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode"""
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break

    content = block[level:].strip()
    return ParentNode(f"h{level}", text_to_children(content))

def code_block_to_html_node(block):
    """Convert a code block to an HTMLNode"""
    lines = block.split("\n")
    content = "\n".join(lines[1:-1])
    code_node = LeafNode("code", content)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode"""
    lines = block.split("\n")
    content = "\n".join([line.strip()[2:] if line.strip().startswith("> ") else line.strip()[1:] if line.strip().startswith(">") else line.strip() for line in lines])
    return ParentNode("blockquote", text_to_children(content))

def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode"""
    items = [line.strip()[2:] for line in block.split("\n") if line.strip()]
    list_items = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode"""
    items = []
    for line in block.split("\n"):
        if line.strip():
            if ". " in line:
                content = line.split(". ", 1)[1]
            elif ".) " in line:
                content = line.split(".) ", 1)[1]
            else:
                content = line
            items.append(content)
    
    list_items = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", list_items)