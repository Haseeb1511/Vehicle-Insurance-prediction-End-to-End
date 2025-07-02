import boto3
from src.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union,List
import os,sys
from src.logger import configure_logger
logger = configure_logger("aws_storage")
from src.exception import MyException
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle
from mypy_boto3_s3.service_resource import Bucket



class SimpleStorageService:

    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    def s3_key_path_available(self, bucket_name, s3_key):
        bucket = self.get_bucket(bucket_name=bucket_name)
        file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
        return len(file_objects) > 0
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False):
                    # Read and decode the object content if decode=True
        func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode else object_name.get()["Body"].read())
            
        # Convert to StringIO if make_readable=True
        conv_func = lambda: StringIO(func()) if make_readable else func()
        return conv_func
    
    def get_bucket(self,bucket_name:str)->Bucket:
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket

    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        bucket  = self.get_bucket(bucket_name)
        file_object = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
        func = lambda x: x[0] if len(x) == 1 else x
        return file_object
    
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        model_file = model_dir + "/" + model_name if model_dir else model_name
        file_object = self.get_file_object(model_file, bucket_name)
        model_obj = self.read_object(file_object, decode=False)
        model = pickle.loads(model_obj)
        return model
    
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            # If folder does not exist, create it
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logger.info("Exited the create_folder method of SimpleStorageService class")

    
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:    
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
        # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                logger.info(f"Removed local file {from_filename} after upload")
            logger.info("Exited the upload_file method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys) from e
        

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        # Save DataFrame to CSV locally and then upload it
        data_frame.to_csv(local_filename, index=None, header=True)
        self.upload_file(local_filename, bucket_filename, bucket_name)



    def get_df_from_object(self, object_: object) -> DataFrame:
        content = self.read_object(object_, make_readable=True)
        df = read_csv(content, na_values="na")
        logger.info("Exited the get_df_from_object method of SimpleStorageService class")
        return df
    
    
    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        csv_obj = self.get_file_object(filename, bucket_name)
        df = self.get_df_from_object(csv_obj)
        logger.info("Exited the read_csv method of SimpleStorageService class")
        return df
    