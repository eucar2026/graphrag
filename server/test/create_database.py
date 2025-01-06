import os

def createFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def createDatabase(dbName):
    createFolder(f"/databases/{dbName}")
    createFolder(f"/databases/{dbName}/files")
    createFolder(f"/databases/{dbName}/index")

createDatabase("test2")