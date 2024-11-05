import ZODB, ZODB.FileStorage
import transaction  # manages the changes made to the objects
from persistent.mapping import PersistentMapping
from HomeWork.HomeWork11.HW11_66011277_Thuwanon_model import Course, Student

# ZODB Database setup
storage = ZODB.FileStorage.FileStorage("mydata.fs")
db = ZODB.DB(storage) 
connection = db.open()  
root = (
    connection.root()
)

if not hasattr(root, "courses"):
    root.courses = PersistentMapping()
if not hasattr(root, "students"):
    root.students = PersistentMapping()


def close_connection():
    connection.close()
    db.close()
