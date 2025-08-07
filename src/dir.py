import os
import shutil


def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_items_to_new_dir("static", "public")


def copy_items_to_new_dir(old_path, new_path):
    items = os.listdir(old_path)

    for item in items:
        current_path = os.path.join(old_path, item)

        if os.path.isfile(current_path):
            shutil.copy(current_path, new_path)
        else:
            copy_path = os.path.join(new_path, item)
            os.mkdir(copy_path)  # public/test
            copy_items_to_new_dir(current_path, copy_path)
