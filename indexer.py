import os
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex, Settings, StorageContext
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

documents = SimpleDirectoryReader("./data").load_data()

llm = OpenAI(temperature=0)
Settings.llm = llm
Settings.chunk_size = 512

graph_store = SimpleGraphStore()
storage_context = StorageContext.from_defaults(graph_store=graph_store)

index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    storage_context=storage_context,
)

storage_context.persist()