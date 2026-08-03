from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")
db=client["studentapidb"]

student_collection=db["students"]
course_collection=db["courses"]
user_collection=db["users"]

student_collection.create_index("email",unique=True)
student_collection.create_index("marks")
student_collection.create_index("course_ids")
student_collection.create_index([("name",1),("marks",-1)])
