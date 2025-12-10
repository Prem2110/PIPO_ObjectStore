import os
from sap_os import download, list_objects

DOWNLOAD_ROOT = "downloads"


def download_all(prefix: str, local_root: str = DOWNLOAD_ROOT):
    """Download all files under a given prefix."""

    files = list_objects(prefix)

    if not files:
        print("No files found.")
        return

    for f in files:
        object_key = f["key"]
        local_path = os.path.join(local_root, object_key)

        # Ensure directories exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download file
        download(object_key, local_path)

        print(f"Saved: {local_path}")


if __name__ == "__main__":
    download_all("demo/")
