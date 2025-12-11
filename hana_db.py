import os
from hdbcli import dbapi
from dotenv import load_dotenv

load_dotenv()
# -----------------------------
# Load HANA configuration
# -----------------------------
load_dotenv()

HANA_ADDRESS = os.getenv("HANA_ADDRESS") or ""
HANA_PORT = int(os.getenv("HANA_PORT") or "443")
HANA_USER = os.getenv("HANA_USER") or ""
HANA_PASSWORD = os.getenv("HANA_PASSWORD") or ""

HANA_SCHEMA = os.getenv("HANA_SCHEMA") or ""
HANA_TABLE = os.getenv("HANA_TABLE") or ""


# -----------------------------
# Connection Handling
# -----------------------------
def get_connection():
    """Create secure encrypted connection to SAP HANA Cloud."""
    return dbapi.connect(
        address=HANA_ADDRESS,
        port=HANA_PORT,
        user=HANA_USER,
        password=HANA_PASSWORD,
        encrypt=True,
        sslValidateCertificate=False
    )


# -----------------------------
# Insert Metadata Row
# -----------------------------
def insert_metadata(metadata: dict):
    """Insert metadata into the table chosen from environment variables."""

    conn = get_connection()
    cursor = conn.cursor()

    if HANA_SCHEMA:
        cursor.execute(f"SET SCHEMA {HANA_SCHEMA}")

    sql = f"""
        INSERT INTO {HANA_TABLE} (
            FILE_ID,
            OBJECT_KEY,
            FILE_NAME,
            MIME_TYPE,
            SIZE,
            UPLOADED_BY
        ) VALUES (?, ?, ?, ?, ?, ?)
    """

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

    print(f"[HANA] Metadata inserted into {HANA_SCHEMA}.{HANA_TABLE} → {metadata['file_id']}")


# -----------------------------
# SET SCHEMA AI_USE_CASES_HDI_DB_1;

# CREATE COLUMN TABLE USER_FILES_METADATA (
#     FILE_ID NVARCHAR(36) PRIMARY KEY,
#     OBJECT_KEY NVARCHAR(500) NOT NULL,
#     FILE_NAME NVARCHAR(255) NOT NULL,
#     MIME_TYPE NVARCHAR(100),
#     SIZE BIGINT,
#     UPLOADED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UPLOADED_BY NVARCHAR(100)
# );
# -----------------------------