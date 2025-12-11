from fastapi import FastAPI, UploadFile, File
from typing import List
from sap_os import upload

app = FastAPI()

UPLOAD_ROOT = "demo"


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded = []

    for file in files:
        # file.filename may contain folder structure from Fiori
        # example: "myfolder/sub/test1.txt"
        filename = file.filename or "uploaded_file"
        object_key = f"{UPLOAD_ROOT}/{filename}"

        # Save temporarily
        temp_path = f"/tmp/{filename.replace('/', '_')}"
        content = await file.read()

        with open(temp_path, "wb") as f:
            f.write(content)

        # Upload to SAP Object Store
        upload(temp_path, object_key)

        uploaded.append(object_key)

    return {"uploaded_files": uploaded}
