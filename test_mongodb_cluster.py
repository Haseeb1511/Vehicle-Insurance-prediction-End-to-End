from pymongo import MongoClient

uri = "mongodb+srv://haseeb15112001:qMbx7IrQY5r9iz0a@cluster0.wjuozl6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["Vehicle_Insurance_project"]
collection = db["Vehicle_data"]

print(collection.find_one())
