import os
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex, Settings, StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

documents = SimpleDirectoryReader("./data").load_data()

llm = OpenAI(temperature=0)
# Settings.llm = llm
# Settings.chunk_size = 512

graph_store = Neo4jGraphStore(
    username="prog2",
    password=os.environ["NEO4J_PASSWORD"],
    url="bolt://localhost:7687",
    database="neo4j",
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    storage_context=storage_context,
)

storage_context.persist()