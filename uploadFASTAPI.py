from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import uuid
import mimetypes
from sap_os import upload_stream
from hana_db import insert_metadata
import uvicorn


UPLOAD_ROOT = "demo"

app = FastAPI(title="File Upload API")


async def prepare_metadata(file: UploadFile, object_key, uploaded_by="api_user"):
    # Read full file to calculate size
    file_bytes = await file.read()
    size = len(file_bytes)

    # Reset pointer for upload_stream
    await file.seek(0)

    return {
        "file_id": str(uuid.uuid4()),
        "object_key": object_key,
        "file_name": file.filename,
        "mime_type": file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream",
        "size": size,
        "uploaded_by": uploaded_by
    }



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    object_key = f"{UPLOAD_ROOT}/{file.filename}".replace("\\", "/")

    # Prepare metadata first (calculates size)
    metadata = await prepare_metadata(file, object_key)

    try:
        upload_stream(file.file, object_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload: {e}")

    insert_metadata(metadata)

    return JSONResponse(
        status_code=201,
        content={"file_name": file.filename, "file_id": metadata["file_id"]}
    )



@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        object_key = f"{UPLOAD_ROOT}/{file.filename}".replace("\\", "/")

        try:
            # Calculate size correctly
            metadata = await prepare_metadata(file, object_key)

            upload_stream(file.file, object_key)

            insert_metadata(metadata)

            results.append({"file_name": file.filename, "file_id": metadata["file_id"]})

        except Exception as e:
            results.append({"file_name": file.filename, "error": str(e)})

    return {"uploaded_files": results}


if __name__ == "__main__":
    uvicorn.run(
        "uploadFASTAPI:app",   # replace yourfilename with the actual Python file name
        host="0.0.0.0",
        port=8000,
        reload=True
    )


