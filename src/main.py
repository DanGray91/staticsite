import os
import shutil
import sys
from textnode import TextNode, TextType
from markdown import extract_title
from md_to_html import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if not basepath.endswith('/'):
        basepath = basepath + '/'

    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)
    
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w') as f:
        f.write(final_html)

def copy_static(source_dir, dest_dir):
    """
    Recursively copy all files from source_dir to dest_dir.
    First deletes the contents of dest_dir if it exists.
    """
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    os.mkdir(dest_dir)
    
    def copy_recursive(current_source, current_dest):
        items = os.listdir(current_source)
        
        for item in items:
            source_path = os.path.join(current_source, item)
            dest_path = os.path.join(current_dest, item)
            
            if os.path.isfile(source_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(source_path, dest_path)
                print(f"Copied file: {source_path} to {dest_path}")
            
            elif os.path.isdir(source_path):
                os.makedirs(dest_path, exist_ok=True)
                print(f"Created directory: {dest_path}")
                copy_recursive(source_path, dest_path)
    
    copy_recursive(source_dir, dest_dir)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(
                entry_path, 
                template_path,  
                os.path.join(dest_dir_path, entry),
                basepath
            )
        elif os.path.isfile(entry_path) and entry_path.endswith(".md"):
            html_filename = entry[:-3] + ".html"
            dest_path = os.path.join(dest_dir_path, html_filename)
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_page(entry_path, template_path, dest_path, basepath)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    output_dir = "docs"
    
    copy_static("static", output_dir)
    
    generate_pages_recursive("content", "template.html", output_dir, basepath)
    
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()
