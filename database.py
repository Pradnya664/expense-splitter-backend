from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="split-expense-app\venv\.env")  # Load from .env file



#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI = "mongodb+srv://splituser:splituser66@cluster0.uht8pze.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("🔍 Loaded MONGO_URI:", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client.splitapp  # Our database
expenses_collection = db.expenses  # We will use this in expenses API
