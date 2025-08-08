import os
import shutil
import sys

from src.copy_dir_contents import copy_static_to_public
from src.markdown_utilities import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"


def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_static_to_public(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "./template.html", dir_path_public, base_path)


if __name__ == "__main__":
    main()
