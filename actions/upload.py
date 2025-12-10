import os
from sap_os import upload

UPLOAD_ROOT = "demo"  # root folder inside Object Store


def upload_action(local_file: str, object_root: str = UPLOAD_ROOT):
    """
    Upload file and preserve local folder structure.
    Example:
       local:  images/cat.png
       remote: demo/images/cat.png
    """

    # Remove leading "./" or "/" for cleanliness
    clean_path = local_file.lstrip("./").lstrip("/")

    # Build remote object key
    object_key = os.path.join(object_root, clean_path).replace("\\", "/")

    upload(local_file, object_key)

    print(f"Uploaded as object key: {object_key}")


if __name__ == "__main__":
    upload_action("test1.txt")
