# THis file convert the mongodb data to pandas Dataframe

import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongodb import MongoDBClient
from src.constant import DATABASE_NAME
from src.exception import MyException
from src.logger import configure_logger
logger = configure_logger("mongo_to_pd")


class VehicleData():
    """
    A class to export MongoDB records as a pandas DataFrame.
    """
    def __init__(self) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
    
    def export_collection_pandas_df(self,collection_name,database_name):
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")

            df = pd.DataFrame(list(collection.find().limit(2000)))    ## This returns a list of documents (dicts)

            print(f"Data fecthed with len: {len(df)}")
            logger.info(f"Data fetched from Mongodb with len: {len(df)}")

            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise MyException(e, sys)
        
