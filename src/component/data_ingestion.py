from src.logger import configure_logger
logger = configure_logger("data_ingestion")
from src.exception import MyException
import os,sys
from src.entity.config_entity import DataIngestionConfig
from src.entity.artificat_entity import DataIngestionArtifact
from src.data_access.vehicle_data import VehicleData
import pandas as pd

from sklearn.model_selection import train_test_split



class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def export_data_into_feature_store(self):
        try:
            my_data = VehicleData()
            dataframe = my_data.export_collection_pandas_df(collection_name="Vehicle_data",database_name="Vehicle_Insurance_project")

            #creating data store path
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            #saving the data
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MyException(e,sys) from e
    
    def split_data(self,dataframe:pd.DataFrame):
        try:
            train_data,test_data = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            #make dir
            train_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(train_dir,exist_ok=True)
            os.makedirs(test_dir,exist_ok=True)

            # save the train and test data
            train_data.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
        except Exception as e:
            raise MyException(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            data = self.export_data_into_feature_store()
            split =self.split_data(data)

            data_ingestion = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion
        except Exception as e:
            raise MyException(e,sys) from e


    