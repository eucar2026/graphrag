import os
import psycopg2
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex, Document
from llama_index.storage.docstore.postgres import PostgresDocumentStore
from llama_index.vector_stores.postgres import PGVectorStore

load_dotenv()

# returns the document store with postgres
def get_document_store():
    return PostgresDocumentStore.from_params(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DATABASE'],
        table_name="documents"
    )

# returns the vector store with postgres
def get_vector_store():
    return PGVectorStore.from_params(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DATABASE'],
        table_name="chunks",
        hybrid_search=True,
        embed_dim=1536, # openai embedding dimension
        hnsw_kwargs={
            "hnsw_m": 16,
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops"
        },
    )

# returns the storage context
def get_storage_context():
    return StorageContext.from_defaults(docstore=get_document_store(), vector_store=get_vector_store())

# returns the vector store index with the existing database
def get_vector_index():
    return VectorStoreIndex.from_vector_store(vector_store=get_vector_store())

# indexes a document in the existing database
def index_document(doc):
    VectorStoreIndex.from_documents([doc], storage_context=get_storage_context(), show_progress=True)

# returns the postgres connection cursor
def get_postgres_connection():
    connection_string = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DATABASE']}"
    conn = psycopg2.connect(connection_string)
    conn.autocommit = True
    return conn.cursor()