#!/usr/bin/env python3

import sys
import os
import shutil

from markdown_converter import extract_markdown_heading, markdown_to_html_nodes


def copy_dir(src_dir: str, dst_dir: str) -> None:
    # Check if source directory exists
    if not os.path.isdir(src_dir):
        raise IsADirectoryError(f"no such directory: '{src_dir}'")
    # Create empty destination directory
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    os.mkdir(dst_dir)

    # Copy directory content recursively
    dir_content = os.listdir(src_dir)
    for name in dir_content:
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                # Create directory, if not existing
                os.mkdir(dst_path)
            copy_dir(src_path, dst_path)
        if os.path.isfile(src_path):
            shutil.copyfile(src_path, dst_path)

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}' as template...")

    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    title = extract_markdown_heading(markdown)
    content = markdown_to_html_nodes(markdown).to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    # Check if markdown directory exists
    if not os.path.isdir(dir_path_content):
        raise IsADirectoryError(f"no such directory: '{dir_path_content}'")
    # Create empty destination directory
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)

    dir_content = os.listdir(dir_path_content)
    for name in dir_content:
        src_path = os.path.join(dir_path_content, name)
        dst_path = os.path.join(dest_dir_path, name)
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                # Create directory, if not existing
                os.mkdir(dst_path)
            generate_pages_recursive(src_path, template_path, dst_path, base_path)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dst_path = dst_path.removesuffix(".md") + ".html"
            generate_page(src_path, template_path, dst_path, base_path)

def clean_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def main() -> int:
    basepath = "/"
    args = sys.argv
    if len(args) > 1:
        basepath = args[1]
    print(args)
    clean_dir("docs/")
    try:
        copy_dir("static/", "docs/")
    except IsADirectoryError as error:
        print(f"Error while copying static files: {error}")
        return -1
    try:
        generate_pages_recursive("content/", "template.html", "docs/", basepath)
    except (FileNotFoundError, IsADirectoryError) as error:
        print(f"Error while generating html pages: {error}")
        return -1

    return 0

if __name__ == "__main__":
    sys.exit(main())