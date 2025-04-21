import os
import PyPDF2
import os.path
import shutil
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex, StorageContext, load_index_from_storage
from postgres import index_document, check_database_tables, get_postgres_connection, get_vector_index
from fastapi import FastAPI, UploadFile, HTTPException

load_dotenv()

app = FastAPI()

def createFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

@app.post("/databases")
def create_database(dbName):
    cursor = check_database_tables()
    cursor.execute("insert into user_databases (db_name) values (%s) returning db_id", (dbName,))
    dbId = cursor.fetchone()[0]
    createFolder(f"/databases/{dbId}")
    createFolder(f"/databases/{dbId}/files")
    return {"success": True}


@app.get("/databases")
def get_databases():
    return os.listdir("/databases")

@app.post("/files")
async def add_files(dbId, files: list[UploadFile]):
    """adds files to selected database and indexes them"""
    try: 
        fileIds = []
        # process the files coming from web server one by one
        for file in files:
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
            # adds file to database and gets file id back to use file id instead of file name to avoid duplicate files
            cursor = check_database_tables()
            cursor.execute("insert into database_files (db_id, file_name) values (%s, %s) returning file_id", (dbId, file.filename))
            fileId = cursor.fetchone()[0]
            print(fileId)

            # save indexed file to files folder
            file_path = f"/databases/{dbId}/files/{fileId}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file.file.close()

            # loads documents that were uploaded by fastapi
            pdf_reader = PyPDF2.PdfReader(file_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                document = Document(
                    text=text.replace('\x00', ''),
                    id_=f"{fileId}_part_{page_num}"
                )

            # insert documents to database
            index_document(dbId, document)
            
            # adds fileid to list to return
            fileIds.append(fileId)
              
        return {"success": True, "fileIds": fileIds}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
@app.get("/files")
def get_files(dbId):
    connection = get_postgres_connection()
    # TODO: SQL injectino attack risk, fix
    connection.execute(f"select file_id,file_name from database_files where db_id = {dbId}")
    return connection.fetchall()

@app.get("/query")
def query_database(dbId, prompt):
    """queries database with given prompt and returns response"""
    # loads existing index
    index = get_vector_index(dbId)
    # queries the index
    query_engine = index.as_query_engine()
    results = query_engine.query(prompt)
    return results.response

@app.delete("/files")
def delete_file(dbId, fileId):
    """deletes a given file from the database"""
    cursor = get_postgres_connection()
    cursor.execute(f"delete from database_files where db_id = %s and file_id = %s", (dbId, fileId))
    cursor.execute(f"delete from data_documents_{dbId} where key like '{fileId}\\_part\\_%'")
    cursor.execute(f"delete from data_chunks_{dbId} where metadata_->>'document_id' like '{fileId}\\_part\\_%'")
    os.remove(f"/databases/{dbId}/files/{fileId}")
    return {"success":True}

@app.delete("/databases")
def delete_database(dbId):
    """deletes a given file from the database"""
    cursor = get_postgres_connection()
    cursor.execute(f"delete from database_files where db_id = %s", (dbId,))
    cursor.execute(f"drop table data_documents_{dbId}")
    cursor.execute(f"drop table data_chunks_{dbId}")
    cursor.execute(f"delete from user_databases where db_id = %s", (dbId,))
    shutil.rmtree(f"/databases/{dbId}")
    return {"success":True}