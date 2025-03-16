import os
import psycopg2
from dotenv import load_dotenv
from llama_index.core import StorageContext, VectorStoreIndex, Document
from llama_index.storage.docstore.postgres import PostgresDocumentStore
from llama_index.vector_stores.postgres import PGVectorStore

load_dotenv()

# returns the document store with postgres
def get_document_store(dbId):
    return PostgresDocumentStore.from_params(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DATABASE'],
        table_name=f"documents_{dbId}"
    )

# returns the vector store with postgres
def get_vector_store(dbId):
    return PGVectorStore.from_params(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DATABASE'],
        table_name=f"chunks_{dbId}",
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
def get_storage_context(dbId):
    return StorageContext.from_defaults(docstore=get_document_store(dbId), vector_store=get_vector_store(dbId))

# returns the vector store index with the existing database
def get_vector_index(dbId):
    return VectorStoreIndex.from_vector_store(vector_store=get_vector_store(dbId))

# indexes a document in the existing database
def index_document(dbId, doc):
    VectorStoreIndex.from_documents([doc], storage_context=get_storage_context(dbId), show_progress=True)

# returns the postgres connection cursor
def get_postgres_connection():
    connection_string = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DATABASE']}"
    conn = psycopg2.connect(connection_string)
    conn.autocommit = True
    return conn.cursor()

# creates the databases table if doesn't exist
def check_database_table(cursor, tableName, tableDef):
    cursor.execute(f"SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{tableName}'")
    record = cursor.fetchone()
    print(record[0])
    if record[0] == 0:
        cursor.execute(f"CREATE TABLE {tableName}({tableDef})")

def check_database_tables():
    cursor = get_postgres_connection()
    check_database_table(cursor, "user_databases", "db_id SERIAL PRIMARY KEY, db_name VARCHAR NOT NULL")
    check_database_table(cursor, "database_files", "file_id SERIAL PRIMARY KEY, db_id int, file_name VARCHAR NOT NULL")
    return cursor