from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os.path
import os

load_dotenv()

def query_database(dbName, prompt):
    """queries database with given prompt and returns response"""
    PERSIST_DIR = f"/databases/{dbName}/index"
    # loads existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    # queries the index
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
    
print(query_database("test","What is bioinformatics? "))