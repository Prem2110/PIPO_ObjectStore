# import os
# import sys
# from sap_os import upload

# UPLOAD_ROOT = "demo"  # root folder inside Object Store


# def upload_single_file(path: str, object_root: str = UPLOAD_ROOT):
#     """Upload one file only."""
#     if not os.path.isfile(path):
#         raise FileNotFoundError(f"{path} is not a valid file")

#     filename = os.path.basename(path)
#     object_key = os.path.join(object_root, filename).replace("\\", "/")

#     upload(path, object_key)
#     print(f"Uploaded file → {object_key}")


# def main():
#     # sys.argv = ["actions.upload", "test1.txt", "test2.txt"]
#     files = sys.argv[1:]

#     if not files:
#         print("Usage: python -m actions.upload <file1> <file2> ...")
#         return

#     for f in files:
#         upload_single_file(f)


# if __name__ == "__main__":
#     main()


import os
import sys
import uuid
import mimetypes

from sap_os import upload
from hana_db import insert_metadata     # ✅ NEW

UPLOAD_ROOT = "demo"  # root folder inside Object Store


def upload_single_file(path: str, object_root: str = UPLOAD_ROOT):
    """Upload one file and store metadata in HANA."""

    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} is not a valid file")

    filename = os.path.basename(path)
    object_key = os.path.join(object_root, filename).replace("\\", "/")

    # 1️⃣ Upload file to Object Store
    upload(path, object_key)
    print(f"Uploaded file → {object_key}")

    # 2️⃣ Prepare metadata for HANA
    metadata = {
        "file_id": str(uuid.uuid4()),
        "object_key": object_key,
        "file_name": filename,
        "mime_type": mimetypes.guess_type(path)[0],
        "size": os.path.getsize(path),
        "uploaded_by": "system"
    }

    # 3️⃣ Insert metadata into HANA
    insert_metadata(metadata)

    print(f"[HANA] Metadata saved → {metadata['file_id']}")


def main():
    files = sys.argv[1:]

    if not files:
        print("Usage: python -m actions.upload <file1> <file2> ...")
        return

    for f in files:
        upload_single_file(f)


if __name__ == "__main__":
    main()