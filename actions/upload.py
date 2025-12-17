import os
from sap_os import upload

UPLOAD_ROOT = "demo"  # root folder inside Object Store


def upload_single_file(local_file: str, object_root: str = UPLOAD_ROOT):
    """Upload a single file and preserve folder structure."""
    clean_path = local_file.lstrip("./").lstrip("/")
    object_key = os.path.join(object_root, clean_path).replace("\\", "/")

    upload(local_file, object_key)
    print(f"Uploaded → {local_file} → {object_key}")


def upload_folder(folder_path: str, object_root: str = UPLOAD_ROOT):
    """Upload all files inside a folder (recursively)."""

    folder_path = folder_path.rstrip("/").rstrip("\\")

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a folder")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)

            # Build remote object key: demo/folder/subfolder/file.ext
            relative_path = os.path.relpath(local_path, folder_path)
            object_key = os.path.join(object_root, folder_path, relative_path).replace("\\", "/")

            upload(local_path, object_key)
            print(f"Uploaded → {local_path} → {object_key}")


def upload_action(path: str):
    """Detect file or folder and upload accordingly."""
    if os.path.isfile(path):
        upload_single_file(path)
    elif os.path.isdir(path):
        upload_folder(path)
    else:
        print(f"Error: {path} is not a valid file or folder")


if __name__ == "__main__":
    upload_action("HR Mini Master")

