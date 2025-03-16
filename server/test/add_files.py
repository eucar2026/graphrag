from dotenv import load_dotenv
from llama_index.core import Document
import PyPDF2
from pathlib import Path
import os.path
import os
# setting path to import postgres library
import sys
# sys.path.append('..')
from postgres import index_document, check_database_tables

load_dotenv()

def add_files(dbId):
    """adds file to selected database and indexes it
    upload file api call is supposed to save the pdf inside the database's temp folder
    """
    # process the files in temp folder one by one
    fileList = os.listdir(f"/databases/{dbId}/temp")
    for file in fileList:
        # adds file to database and gets file id back to use file id instead of file name to avoid duplicate files
        cursor = check_database_tables()
        cursor.execute("insert into database_files (db_id, file_name) values (%s, %s) returning file_id", (dbId, file))
        fileId = cursor.fetchone()[0]
        print(fileId)
        file_path = f"/databases/{dbId}/temp/{file}"
        print(file_path)
        # loads documents that were put in temp folder by file upload api
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
        
        # moves indexed files to files folder
        os.rename(file_path, f"/databases/{dbId}/files/{file}")

add_files(3)