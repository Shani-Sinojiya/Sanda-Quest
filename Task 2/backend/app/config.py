import os
from motor.motor_asyncio import AsyncIOMotorClient

# Directories
UPLOAD_DIR = './uploads'
OUTPUT_DIR = './app/static/outputs'
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# MongoDB setup
MONGO_URI = "mongodb+srv://python:1234567890@cluster.kvnyt.mongodb.net/"
DB_NAME = "sandalquest"
COLLECTION_NAME = "communications"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
