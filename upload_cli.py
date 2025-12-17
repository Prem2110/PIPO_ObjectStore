import os
import uuid
import mimetypes
from sap_os import upload_stream
from hana_db import insert_metadata

UPLOAD_ROOT = "demo"


def prepare_metadata(file_path: str, object_key: str, uploaded_by="cli_user"):
    size = os.path.getsize(file_path)

    return {
        "file_id": str(uuid.uuid4()),
        "object_key": object_key,
        "file_name": os.path.basename(file_path),
        "mime_type": mimetypes.guess_type(file_path)[0]
        or "application/octet-stream",
        "size": size,
        "uploaded_by": uploaded_by
    }


def upload_file(file_path: str, base_folder: str):
    # Build relative path (preserve folder structure)
    rel_path = os.path.relpath(file_path, base_folder)
    rel_path = rel_path.replace("\\", "/")

    object_key = f"{UPLOAD_ROOT}/{rel_path}"

    print(f"⬆ Uploading: {file_path}")
    print(f"   → Object key: {object_key}")

    with open(file_path, "rb") as f:
        upload_stream(f, object_key)

    metadata = prepare_metadata(file_path, object_key)
    insert_metadata(metadata)


def upload_folder(folder_path: str):
    folder_path = os.path.abspath(folder_path)

    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            upload_file(full_path, folder_path)

    print("\n✅ Folder upload completed.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage:")
        print("  python upload_cli.py <file_or_folder_path>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        upload_file(path, os.path.dirname(path) or ".")
    elif os.path.isdir(path):
        upload_folder(path)
    else:
        print("❌ Invalid path:", path)
