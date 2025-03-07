import os
import subprocess
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import logging

# Azure Blob Storage configuration
STORAGE_ACCOUNT_URL = os.getenv("STORAGE_ACCOUNT_URL")  # e.g., https://<storage_account>.blob.core.windows.net
STORAGE_ACCOUNT_KEY = os.getenv("STORAGE_ACCOUNT_KEY")
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "psql-backups")

# Temporary directory for backups
BACKUP_DIR = "/tmp/psql_backups"

# List of databases to back up
DBS = [
    {"name": "production_db", "url": os.getenv("PRODUCTION_DB_URL")},
    {"name": "test_db", "url": os.getenv("TEST_DB_URL")},
]

def backup_database(db_name, db_url):
    """Back up a PostgreSQL database using pg_dump."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    backup_file = f"{BACKUP_DIR}/{db_name}_backup_{timestamp}.sql"

    try:
        # Run pg_dump command
        subprocess.run(
            ["pg_dump", db_url, "-f", backup_file],
            check=True
        )
        logging.info(f"Backup successful: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during backup for {db_name}: {e}")
        return None

def upload_to_blob(file_path, blob_name):
    """Upload a file to Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=STORAGE_ACCOUNT_KEY)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        logging.info(f"Uploaded to Azure Blob Storage: {blob_name}")
    except Exception as e:
        logging.error(f"Error uploading to Blob Storage: {e}")

def main(mytimer):
    """Main function to back up databases and upload to Azure Blob Storage."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    for db in DBS:
        logging.info(f"Starting backup for database: {db['name']}")
        backup_file = backup_database(db["name"], db["url"])
        if backup_file:
            blob_name = os.path.basename(backup_file)
            upload_to_blob(backup_file, blob_name)
            os.remove(backup_file)  # Clean up local backup file
