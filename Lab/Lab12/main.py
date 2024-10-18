import ZODB, ZODB.FileStorage
import transaction  # manages the changes made to the objects
from persistent.mapping import (
    PersistentMapping,
)  # special dictionary-like structure that stores persistent objects
from model import Course, Student  # Importing models from models.py
# ZODB Database setup
storage = ZODB.FileStorage.FileStorage("mydata.fs") # create a file storage
db = ZODB.DB(storage)  # init the ZODB database
connection = db.open()  # open connection to the database
root = connection.root()
if not hasattr(root, "courses"):
    root.courses = PersistentMapping()
if not hasattr(root, "students"):
    root.students = PersistentMapping()


# Closing the ZODB connection (can be called from test.py when done)
def close_connection():
    connection.close()
    db.close()