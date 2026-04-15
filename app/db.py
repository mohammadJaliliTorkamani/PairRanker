from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client.casey_db

def get_db():
    return db