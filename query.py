import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext

from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.graph_stores.neo4j import Neo4jPGStore
from llama_index.core.storage.index_store import SimpleIndexStore

from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)

from dotenv import load_dotenv

load_dotenv()

#documents = SimpleDirectoryReader("data").load_data()
#index = VectorStoreIndex.from_documents(documents)

#from llama_index.indices.propterty_graph import SchemaLLMPathExtractor

graph_store = Neo4jPGStore(
    username="prog2",
    password=os.environ["NEO4J_PASSWORD"],
    url="bolt://localhost:7687",
    database="neo4j",
)

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(),
    graph_store=graph_store,
    #index_store=SimpleIndexStore.from_persist_dir(),
)

index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine(
    include_text=False, response_mode="tree_summarize",
    verbose=True
)
response = query_engine.query("When was react rewritten? ")
print(response)