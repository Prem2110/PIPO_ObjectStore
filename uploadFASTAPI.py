from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import zipfile
import tempfile
import os
import uuid
import mimetypes

from sap_os import upload_stream
from hana_db import insert_metadata

# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------
UPLOAD_ROOT = "demo"

app = FastAPI(title="ZIP Folder Upload API")

# ------------------------------------------------------
# ZIP-ONLY UPLOAD ROUTE
# ------------------------------------------------------
@app.post("/upload")
async def upload_zip(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files received")

    results = []

    for file in files:
        if not file.filename.lower().endswith(".zip"):
            raise HTTPException(
                status_code=400,
                detail=f"Only ZIP files are allowed: {file.filename}"
            )

        try:
            zip_root = os.path.splitext(file.filename)[0]  # 🔑 ROOT FOLDER NAME

            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, file.filename)

                # Save ZIP
                with open(zip_path, "wb") as f:
                    f.write(await file.read())

                # Extract ZIP
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(tmpdir)

                # Walk extracted files
                for root, _, filenames in os.walk(tmpdir):
                    for fname in filenames:
                        full_path = os.path.join(root, fname)

                        # Skip zip file itself
                        if full_path == zip_path:
                            continue

                        rel_path = os.path.relpath(full_path, tmpdir)
                        rel_path = rel_path.replace("\\", "/")

                        # ✅ PRESERVE ZIP ROOT FOLDER
                        object_key = f"{UPLOAD_ROOT}/{zip_root}/{rel_path}"

                        with open(full_path, "rb") as f:
                            upload_stream(f, object_key)

                        metadata = {
                            "file_id": str(uuid.uuid4()),
                            "object_key": object_key,
                            "file_name": os.path.basename(rel_path),
                            "mime_type": mimetypes.guess_type(fname)[0]
                            or "application/octet-stream",
                            "size": os.path.getsize(full_path),
                            "uploaded_by": "api_user"
                        }

                        insert_metadata(metadata)

                        results.append({
                            "file_name": metadata["file_name"],
                            "file_id": metadata["file_id"],
                            "object_key": object_key
                        })

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {
        "uploaded_count": len(results),
        "items": results
    }

