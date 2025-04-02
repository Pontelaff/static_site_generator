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

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}' as template...")

    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    title = extract_markdown_heading(markdown)
    content = markdown_to_html_nodes(markdown).to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html)

def clean_public_dir() -> None:
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public")

def main() -> int:
    clean_public_dir()
    try:
        copy_dir("static/", "public/")
    except IsADirectoryError as error:
        print(f"Error while copying static files: {error}")
        return -1
    try:
        generate_page("content/index.md", "template.html", "public/index.html")
    except FileNotFoundError as error:
        print(f"Error while generating html page: {error}")
        return -1

    return 0

if __name__ == "__main__":
    sys.exit(main())