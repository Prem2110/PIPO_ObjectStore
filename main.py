# main.py
import uvicorn
from uploadFASTAPI import app as upload_app
from listFASTAPI import app as list_app
from fastapi import FastAPI

app = FastAPI(title="Unified Object Store API")

app.mount("/upload-api", upload_app)
app.mount("/list-api", list_app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
