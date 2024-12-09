import os
from llama_index.core import SimpleDirectoryReader, Settings, StorageContext, PropertyGraphIndex
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor
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

kg_extractor = SimpleLLMPathExtractor(llm=llm)

index = PropertyGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    kg_extractors=[kg_extractor]
)

storage_context.persist()