import os
import shutil


def copy_static_to_public(old_path, new_path):
    items = os.listdir(old_path)

    if not os.path.exists(new_path):
        os.mkdir(new_path)

    for item in items:
        current_path = os.path.join(old_path, item)

        if os.path.isfile(current_path):
            shutil.copy(current_path, new_path)
        else:
            copy_path = os.path.join(new_path, item)
            os.mkdir(copy_path)  # public/test
            copy_static_to_public(current_path, copy_path)
