from typing import Union

from fastapi import FastAPI

import os
from postgres import check_database_tables

app = FastAPI()

def createFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

@app.post("/databases")
def create_database(dbName):
    cursor = check_database_tables()
    cursor.execute("insert into user_databases (db_name) values (%s) returning db_id", (dbName,))
    dbId = cursor.fetchone()[0]
    createFolder(f"/databases/{dbId}")
    createFolder(f"/databases/{dbId}/files")
    createFolder(f"/databases/{dbId}/temp")
    return {"success": True}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}