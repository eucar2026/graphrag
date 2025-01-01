import os
from llama_index.core import StorageContext, load_index_from_storage

from dotenv import load_dotenv

load_dotenv()

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do after he came to the U.S.? ")
print(response)