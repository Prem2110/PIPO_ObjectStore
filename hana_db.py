import os
from hdbcli import dbapi
from dotenv import load_dotenv

load_dotenv()

HANA_ADDRESS = os.getenv("HANA_ADDRESS") or ""
HANA_PORT = int(os.getenv("HANA_PORT") or "443")
HANA_USER = os.getenv("HANA_USER") or ""
HANA_PASSWORD = os.getenv("HANA_PASSWORD") or ""
HANA_SCHEMA = os.getenv("HANA_SCHEMA") or ""
HANA_TABLE = os.getenv("HANA_TABLE") or ""


def get_connection():
    return dbapi.connect(
        address=HANA_ADDRESS,
        port=HANA_PORT,
        user=HANA_USER,
        password=HANA_PASSWORD,
        encrypt=True,
        sslValidateCertificate=False
    )


def insert_metadata(metadata: dict):
    conn = get_connection()
    cursor = conn.cursor()

    if HANA_SCHEMA:
        cursor.execute(f'SET SCHEMA "{HANA_SCHEMA}"')

    sql = f'''
        INSERT INTO "{HANA_TABLE}" (
            "FILE_ID",
            "OBJECT_KEY",
            "FILE_NAME",
            "MIME_TYPE",
            "SIZE",
            "UPLOADED_BY"
        ) VALUES (?, ?, ?, ?, ?, ?)
    '''

    params = (
        metadata["file_id"],
        metadata["object_key"],
        metadata["file_name"],
        metadata["mime_type"],
        metadata["size"],
        metadata["uploaded_by"]
    )

    cursor.execute(sql, params)
    conn.commit()

    cursor.close()
    conn.close()

    print(f"[HANA] Metadata inserted → {metadata['file_id']}")
