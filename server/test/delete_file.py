from dotenv import load_dotenv
import os
from postgres import get_postgres_connection

load_dotenv()

def delete_file(dbId, fileId):
    """deletes a given file from the database"""
    cursor = get_postgres_connection()
    cursor.execute(f"delete from database_files where db_id = %s and file_id = %s", (dbId, fileId))
    cursor.execute(f"delete from data_documents_{dbId} where key like '{fileId}\\_part\\_%'")
    cursor.execute(f"delete from data_chunks_{dbId} where metadata_->>'document_id' like '{fileId}\\_part\\_%'")
    os.remove(f"/databases/{dbId}/files/{fileId}")

delete_file(4,2)