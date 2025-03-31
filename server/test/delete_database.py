from dotenv import load_dotenv
import shutil
from postgres import get_postgres_connection

load_dotenv()

def delete_database(dbId):
    """deletes a given file from the database"""
    cursor = get_postgres_connection()
    cursor.execute(f"delete from database_files where db_id = %s", (dbId,))
    cursor.execute(f"drop table data_documents_{dbId}")
    cursor.execute(f"drop table data_chunks_{dbId}")
    cursor.execute(f"delete from user_databases where db_id = %s", (dbId,))
    shutil.rmtree(f"/databases/{dbId}")

delete_database(3)