import numpy as np
import pandas as pd
import os,sys,json
from src.logger import configure_logger
logger = configure_logger("DataValidation")
from src.exception import MyException
from src.entity.artificat_entity import DataValidationArtifact,DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig
from src.utils.main import read_yaml_file
from src.constant import SCHEMA_FILE_PATH

class DataValidation:

    def __init__(self,data_ingestion_artificat:DataIngestionArtifact,data_validation_config:DataValidationConfig):

        self.data_ingestion_artificat = data_ingestion_artificat 
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)


    def validate_no_of_column(self,dataframe:pd.DataFrame):
        status = len(dataframe.columns)==len(self._schema_config["columns"])
        return status
    
    def is_column_exist(self,dataframe:pd.DataFrame):
        logger.info("Checking if any column is missing....")
        try:
            dataframe_column = dataframe.columns
            logger.info(f"Columns in DataFrame are: {dataframe_column}")
            missing_numerical_column = []
            missing_categorical_column = []

            #Numerical column validation
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_column:
                    missing_numerical_column.append(column)
            if len(missing_numerical_column)> 0:
                logger.info(f"Missing numerical column {missing_numerical_column}")

            #categorical column validation
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_column:
                    missing_categorical_column.append(column)
            if len(missing_categorical_column)>0:
                logger.info(f"Missing categorical column {missing_categorical_column}")

            return False if len(missing_categorical_column)>0 or len(missing_numerical_column)>0 else True
        except Exception as e:
            raise MyException(e,sys) from e
        

    @staticmethod
    def read_data(file_path):
        return pd.read_csv(file_path)
    

    def initiate_data_validation(self):
        try:
            logger.info("Starting initiate data validation  ")
            validation_error_msg = ""
            train_df,test_df  = (DataValidation.read_data(self.data_ingestion_artificat.trained_file_path),DataValidation.read_data(self.data_ingestion_artificat.test_file_path))

            #train dataframe validation
            # Number of columns
            status = self.validate_no_of_column(dataframe=train_df)
            if not status:
                validation_error_msg += "Column count mismatch in train dataframe.\n"

            # Columns existence
            status = self.is_column_exist(dataframe=train_df)
            if not status:
                validation_error_msg += "Missing columns in train dataframe.\n"

            # Same for test_df
            status = self.validate_no_of_column(dataframe=test_df)
            if not status:
                validation_error_msg += "Column count mismatch in test dataframe.\n"

            status = self.is_column_exist(dataframe=test_df)
            if not status:
                validation_error_msg += "Missing columns in test dataframe.\n"

            validation_status = len(validation_error_msg)==0

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path= self.data_validation_config.validation_report_file_path
            )

            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            validation_report = {
                "validation_status":validation_status,
                "message":validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path,"w") as f:
                json.dump(validation_report,f)

            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        