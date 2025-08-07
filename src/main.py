import os
import shutil

from src.dir import copy_static_to_public
from src.markdown_utilities import generate_page

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_static_to_public(dir_path_static, dir_path_public)
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
