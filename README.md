# PIPO Object Store Utility (SAP Object Store)

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

## 🔧 Installation
## uv environment
1. Initalise uv: **uv init**
2. Create a new Virtual environment: **uv venv .venv**
3. activate environment: **.venv\Scripts\activate**
4. install dependencies: **uv add -r requirements.txt**


## Install dependancies
    ` pip install -r requirements.txt `

## ▶️ Usage

``` python
python -m actions.upload

