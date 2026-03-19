import os

from htmlnode import HTMLNode
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    print("Extracting title")
    split_newline = markdown.split("\n")

    for line in split_newline:
        if line.startswith("# "):
            split_space = line.split(" ")
            text = " ".join(split_space[1:])
            return text.strip()
        
    raise Exception(f"Missing H1/title in markdown: {markdown}")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_file_content = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    html_node = markdown_to_html_node(markdown_file_content)
    content = html_node.to_html()
    title = extract_title(markdown_file_content)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    if not os.path.exists(dest_path):
        directory = os.path.dirname(dest_path)
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    print(f"Finding all files from {dir_path_content}")
    for file in content_list:
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, basepath)
    return