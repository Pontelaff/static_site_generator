#!/usr/bin/env python3

import sys
import os
import shutil


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

def main() -> int:
    copy_dir("static/", "public/")
    return 0

if __name__ == "__main__":
    sys.exit(main())