import os

database = "test"
fileList = os.listdir(f"/databases/{database}/files")
for file in fileList:
    print(file)