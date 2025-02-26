# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# MongoDB connection URL (from environment variables or default)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# Initialize MongoDB client
try:
    client = AsyncIOMotorClient(MONGODB_URL)
    db: AsyncIOMotorDatabase = client["test_report_db"]  # Database name
    print("✅ Successfully connected to MongoDB.")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")

def get_collection(collection_name: str):
    """Retrieve a collection from the MongoDB database."""
    return db[collection_name]