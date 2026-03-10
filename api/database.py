from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "flight_price_prediction")

class Database:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB"""
        try:
            cls.client = AsyncIOMotorClient(
                MONGODB_URI,
                server_api=ServerApi('1')
            )
            # Verify connection
            await cls.client.admin.command('ping')
            print(f"✅ Successfully connected to MongoDB!")
            print(f"📊 Database: {DATABASE_NAME}")
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise e
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("🔌 MongoDB connection closed")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.client[DATABASE_NAME]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection from database"""
        db = cls.get_database()
        return db[collection_name]

# Async context manager for database operations
async def get_database():
    """Dependency for getting database instance"""
    return Database.get_database()

# Collection names
FLIGHTS_COLLECTION = "flights"
PREDICTIONS_COLLECTION = "predictions"
