from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os.path
import os
from postgres import get_vector_index

load_dotenv()

def query_database(dbId, prompt):
    """queries database with given prompt and returns response"""
    # loads existing index
    index = get_vector_index(dbId)
    # queries the index
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
    
print(query_database(3,"What is bioinformatics? "))