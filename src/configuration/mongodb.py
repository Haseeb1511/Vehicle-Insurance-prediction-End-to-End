import sys
import os
import pymongo
import certifi
from dotenv import load_dotenv
from src.exception import MyException
from src.logger import logging
from src.constant import DATABASE_NAME, MONGODB_URL_KEY

# Load environment variables from .env file
load_dotenv()

# Get CA file to avoid SSL issues
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes
    ----------
    client : MongoClient
        Shared PyMongo client instance.
    database : Database
        The specific database instance.
    """
    client = None  # Class-level shared client

    def __init__(self, database_name: str = DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                # Load MongoDB URL from env
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if not mongo_db_url:
                    raise Exception("Environment variable for MongoDB URL is not set.")

                # Create PyMongo client
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca,serverSelectionTimeoutMS=50000)
                logging.info("Successfully created MongoDB client.")

            # Use the shared client
            self.client = MongoDBClient.client

            # Get the specific database
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info(f"Connected to MongoDB database: {database_name}")

        except Exception as e:
            raise MyException(e, sys)
