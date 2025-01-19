from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os.path
import os

load_dotenv()

def database_indexed(dbName):
    """Check if database was indexed before"""
    files = os.listdir(f"/databases/{dbName}/index")
    return len(files) != 0

def add_files(dbName):
    """adds file to selected database and indexes it
    upload file api call is supposed to save the pdf inside the database's temp folder
    """
    # loads documents that were put in temp folder by file upload api
    documents = SimpleDirectoryReader(f"/databases/{dbName}/temp").load_data()

    # if database was not indexed before, create dabatase with LlamaIndex
    PERSIST_DIR = f"/databases/{dbName}/index"
    if not database_indexed(dbName):
        # creates index with new documents
        index = VectorStoreIndex.from_documents(documents)
    else: 
        # loads existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        for d in documents:
            index.insert(document = d)
    
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    
    # moves indexed files to files folder
    fileList = os.listdir(f"/databases/{dbName}/temp")
    for file in fileList:
        os.rename(f"/databases/{dbName}/temp/{file}", f"/databases/{dbName}/files/{file}")

add_files("test")