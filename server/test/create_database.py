import os
from postgres import check_databases_table

def createFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def createDatabase(dbName):
    cursor = check_databases_table()
    cursor.execute("insert into user_databases (db_name) values (%s) returning db_id", (dbName,))
    dbId = cursor.fetchone()[0]
    createFolder(f"/databases/{dbId}")
    createFolder(f"/databases/{dbId}/files")
    createFolder(f"/databases/{dbId}/temp")

createDatabase("test4")