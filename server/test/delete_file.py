from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os.path
import os

load_dotenv()

def delete_file(dbName, fileName):
    """deletes a given file from the database"""
    PERSIST_DIR = f"/databases/{dbName}/index"
    "delete from data_documents_3 where key like '1_part%'"
    # loads existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    # deletes file from index, file name should be id
    index.delete_ref_doc(f"{PERSIST_DIR}/{fileName}", delete_from_docstore=True)
    index.storage_context.persist()
    # afterward, delete file

delete_file("test",'C:\\databases\\test\\temp\\abramov.txt')