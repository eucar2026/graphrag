from dotenv import load_dotenv
from llama_index.core import Document
import PyPDF2
from pathlib import Path
import os.path
import os
# setting path to import postgres library
import sys
# sys.path.append('..')
from postgres import index_document

load_dotenv()

def add_files(dbId):
    """adds file to selected database and indexes it
    upload file api call is supposed to save the pdf inside the database's temp folder
    """
    # process the files in temp folder one by one
    fileList = os.listdir(f"/databases/{dbId}/temp")
    for file in fileList:
        # loads documents that were put in temp folder by file upload api
        file_path = f"/databases/{dbId}/temp/{file}"
        pdf_reader = PyPDF2.PdfReader(file_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            document = Document(
                text=text.replace('\x00', ''),
                id_=f"{file}_part_{page_num}"
            )

            # insert documents to database
            index_document(dbId, document)
        
        # moves indexed files to files folder
        os.rename(file_path, f"/databases/{dbId}/files/{file}")

add_files(3)