# PIPO Object Store

A lightweight Python utility to **upload**, **download**, and **list files** in **SAP Object Store** (S3-compatible).

This repository is designed for:
- Simple file operations (upload, download, list)
- Safe credential handling
- Clean modular structure

---

## Features

- Upload files to SAP Object Store
- Download single or **all files under a prefix**
- List files in a directory as a **tree view**
- Uses `.env` for secure credential management
- Clean, modular Python package (`actions/` folder)

---

## Project Structure
```
PIPO_OBJECTSTORE/
│
├── actions/
│ ├── init.py
│ ├── upload.py
│ ├── download.py
│ └── list_files.py
│
├── downloads/ # list of downloaded files
├── sap_os.py # core logic (upload/download/list) 

```

## 🔧 Installation
## uv environment
1. Initalise uv: **uv init**
2. Create a new Virtual environment: **uv venv .venv**
3. activate environment: **.venv\Scripts\activate**


## Install dependancies
``` python
uv add -r requirements.txt
```

## 🔐 Environment Variables (.env)
Create a .env file in the project root:

```env
# Write permissions (UPLOAD)
WRITE_ACCESS_KEY_ID=YOUR_WRITE_KEY
WRITE_SECRET_ACCESS_KEY=YOUR_WRITE_SECRET

# Read permissions (DOWNLOAD + LIST)
READ_ACCESS_KEY_ID=YOUR_READ_KEY
READ_SECRET_ACCESS_KEY=YOUR_READ_SECRET

# Shared configuration
BUCKET_NAME=hcp-xxxxxxx-yyyy-yyyy
REGION=us-east-1
HOST=s3.amazonaws.com
```
---
## ▶️ Usage
To run upload.py
``` python
python -m actions.upload
```

To run download.py
``` python
python -m actions.download
```
To run list_files.py
``` python
python -m actions.list_files
```
---

## HANA DB
```env
HANA_ADDRESS=
HANA_PORT=443
HANA_USER=
HANA_PASSWORD=
HANA_SSL=true
HANA_ENCRYPT=true
HANA_SCHEMA=
HANA_TABLE=
```