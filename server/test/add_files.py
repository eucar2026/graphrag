from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
import os.path
import os
# setting path to import postgres library
import sys
# sys.path.append('..')
from postgres import index_document

load_dotenv()

def add_files(dbName):
    """adds file to selected database and indexes it
    upload file api call is supposed to save the pdf inside the database's temp folder
    """
    # loads documents that were put in temp folder by file upload api
    documents = SimpleDirectoryReader(f"/databases/{dbName}/temp", filename_as_id=True).load_data()
    print(documents)

    # insert documents to database
    for doc in documents:
        index_document(doc)
    
    # moves indexed files to files folder
    fileList = os.listdir(f"/databases/{dbName}/temp")
    for file in fileList:
        os.rename(f"/databases/{dbName}/temp/{file}", f"/databases/{dbName}/files/{file}")

add_files("test")