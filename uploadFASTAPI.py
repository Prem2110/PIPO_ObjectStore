from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from fastapi.responses import JSONResponse
import uuid
import mimetypes
from sap_os import upload_stream
from hana_db import insert_metadata
import uvicorn

UPLOAD_ROOT = "demo"

app = FastAPI(title="Universal File & Folder Upload API")


# ------------------------------------------------------
# METADATA 
# ------------------------------------------------------
async def prepare_metadata(file: UploadFile, object_key, uploaded_by="api_user"):
    file_bytes = await file.read()
    size = len(file_bytes)
    await file.seek(0)

    return {
        "file_id": str(uuid.uuid4()),          
        "object_key": object_key,                
        "file_name": file.filename,              
        "mime_type": file.content_type
        or mimetypes.guess_type(file.filename)[0]
        or "application/octet-stream",
        "size": size,                            
        "uploaded_by": uploaded_by              
    }


# ======================================================
# UNIVERSAL UPLOAD ROUTE (FILES + FOLDERS)
# ======================================================
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files received")

    results = []

    for file in files:
        # Preserve folder structure if present
        clean_path = file.filename.lstrip("./").lstrip("/")
        object_key = f"{UPLOAD_ROOT}/{clean_path}".replace("\\", "/")

        try:
            metadata = await prepare_metadata(file, object_key)

            # Upload to Object Store
            upload_stream(file.file, object_key)

            # Insert metadata 
            insert_metadata(metadata)

            results.append({
                "file_name": file.filename,
                "file_id": metadata["file_id"],
                "object_key": object_key
            })

        except Exception as e:
            results.append({
                "file_name": file.filename,
                "error": str(e)
            })

    return JSONResponse(
        status_code=201,
        content={
            "uploaded_count": len(results),
            "items": results
        }
    )


