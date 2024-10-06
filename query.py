from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext

from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.graph_stores import SimpleGraphStore
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

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(),
    graph_store=SimpleGraphStore.from_persist_dir(),
    index_store=SimpleIndexStore.from_persist_dir(),
)

index = load_index_from_storage(storage_context)

#entities = Literal["PERSON", "PLACE", "THING"]
#relations = Literal["PART_OF", "HAS", "IS_A"]
#SCHEMA = {
#    "PERSON": ["PART_OF", "HAS", "IS_A"],
#    "PLACE": ["PART_OF", "HAS"],
#    "THING": ["IS_A"],
#}

#kg_extractor = SchemaLLMPathExtractor(
#    llm=llm,
#    possible_entities=entities,
#    possible_relations=relations,
#    kg_validation_schema=schema,
#    strict=True,
#)

query_engine = index.as_query_engine(
    include_text=False, response_mode="tree_summarize",
    verbose=True
)
response = query_engine.query("Where was Ethan born? ")
print(response)

#seperate this into index and query programs
#look back at original base rag doc for how to query
#replace combined querying and indexing in indexer with seperate programs