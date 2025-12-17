from fastapi import FastAPI, Query
from typing import Optional, List, Dict
from datetime import datetime
from sap_os import list_objects
from hdbcli import dbapi
import uvicorn
import os
from dotenv import load_dotenv

# ------------------------------------------------------
# ENV + APP
# ------------------------------------------------------
load_dotenv()

app = FastAPI(title="Object Store List API")

LIST_ROOT = "demo"   # ✅ FIXED ROOT (same as upload)

# ------------------------------------------------------
# HANA CONNECTION
# ------------------------------------------------------
def get_hana_connection():
    return dbapi.connect(
        address=os.getenv("HANA_ADDRESS"),
        port=int(os.getenv("HANA_PORT")),
        user=os.getenv("HANA_USER"),
        password=os.getenv("HANA_PASSWORD"),
        currentSchema=os.getenv("HANA_SCHEMA"),
        autocommit=True
    )

# ------------------------------------------------------
# UTILS
# ------------------------------------------------------
def readable_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

# ------------------------------------------------------
# FETCH FILE_IDs FROM METADATA (BULK)
# ------------------------------------------------------
def get_file_metadata_by_object_keys(object_keys: List[str]) -> Dict[str, Dict]:
    if not object_keys:
        return {}

    placeholders = ",".join(["?"] * len(object_keys))
    table = os.getenv("HANA_TABLE")

    conn = get_hana_connection()
    cursor = conn.cursor()

    cursor.execute(
        f'''
        SELECT "OBJECT_KEY", "FILE_ID", "FILE_NAME"
        FROM "{table}"
        WHERE "OBJECT_KEY" IN ({placeholders})
        ''',
        object_keys
    )

    result = {
        row[0]: {
            "file_id": row[1],
            "file_name": row[2]
        }
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    return result


# ------------------------------------------------------
# LIST FILES API
# ------------------------------------------------------
@app.get("/files")
def list_files(prefix: Optional[str] = Query(None, description="Subfolder inside demo/")):
    # --------------------------------------------------
    # Build final prefix (fixed root)
    # --------------------------------------------------
    if prefix:
        final_prefix = f"{LIST_ROOT}/{prefix.lstrip('/')}".rstrip("/") + "/"
    else:
        final_prefix = LIST_ROOT.rstrip("/") + "/"

    # --------------------------------------------------
    # List objects from Object Store
    # --------------------------------------------------
    objects = list_objects(final_prefix)

    if not objects:
        return {
            "prefix": final_prefix,
            "count": 0,
            "files": []
        }

    # --------------------------------------------------
    # Collect object keys
    # --------------------------------------------------
    object_keys = [obj["key"] for obj in objects if "key" in obj]

    if not object_keys:
        return {
            "prefix": final_prefix,
            "count": 0,
            "files": []
        }

    # --------------------------------------------------
    # Fetch metadata from HANA (file_id + original file_name)
    # --------------------------------------------------
    metadata_map = get_file_metadata_by_object_keys(object_keys)

    files = []

    # --------------------------------------------------
    # Build response
    # --------------------------------------------------
    for obj in objects:
        key = obj.get("key")
        size = int(obj.get("size", 0))

        #  Skip folder marker objects
        if key.endswith("/") and size == 0:
            continue

        meta = metadata_map.get(key)
        if not meta:
            continue  #  Skip unmanaged files

        last_modified = obj.get("last_modified")
        if isinstance(last_modified, datetime):
            uploaded_time = last_modified.astimezone().isoformat()
        else:
            uploaded_time = None

        files.append({
            "file_id": meta["file_id"],            # ✅ PRIMARY KEY
            "file_name": meta["file_name"],        # ✅ ORIGINAL FILE NAME
            "size_bytes": size,
            "size_readable": readable_size(size),
            "type": meta["file_name"].split(".")[-1]
                    if "." in meta["file_name"] else "-",
            "uploaded_time": uploaded_time
        })

    return {
        "prefix": final_prefix,
        "count": len(files),
        "files": files
    }
