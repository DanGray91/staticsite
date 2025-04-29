import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split('\n')
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if len(lines) > 0:
        is_ordered_list = True
        for i, line in enumerate(lines):
            if not re.match(f"^{i+1}\\. ", line):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split('\n\n')]
    blocks = [block for block in blocks if block]
    return blocks

def extract_title(markdown):
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("No h1 header found in markdown")
        

