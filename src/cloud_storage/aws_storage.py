import boto3
from src.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union,List
import os,sys
from pandas import DataFrame,read_csv
import pickle
from botocore.exceptions import ClientError

from src.logger import configure_logger
logging = configure_logger("aws_configure")
from src.exception import MyException


class SimpleStorageService:

    def __init__(self):
        """
        Initializes the SimpleStorageService instance with S3 resource and client
        from the S3Client class.
        """
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    def s3_key_path_avaliable(self,bucket_name, s3_key):
        """Checks if a specified S3 key path (file path) is available in the specified bucket"""
        bucket = self.get_bucket(bucket_name)
        file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
        return len(file_objects)>0
    
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False):
        """Read object inside S3 bucke like model"""
        try:
            func = (lambda:object_name.get()["Body"].read().decode()
            if decode else object_name.get()["Body"].read()
            )
            # Convert to StringIO if make_readable=True
            conv_func = lambda: StringIO(func()) if make_readable else func()
            # logging.info("Exited the read_object method of SimpleStorageService class")
            return conv_func()
        except Exception as e:
            raise MyException(e, sys) from e
    

    def get_bucket(self,bucket_name:str):
        """Retrieves the S3 bucket object based on the provided bucket name."""
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket
    
    def get_file_obj(self,file_name,bucket_name)->Union[List[object], object]:
        """Retrieves the file object(s) from the specified bucket based on the filename."""
        bucket = self.get_bucket(bucket_name)
        file_objects = [file_object for file_object in bucket.objects.filter(Prefix=file_name)]
        func = lambda x: x[0] if len(x)==1 else x
        file_obj = func(file_objects)
        return file_obj
    

    def load_model(self,model_name,bucket_name,model_dir):
        """ Loads model from the specified S3 bucket."""

        model_file = model_dir + "/" + model_name if model_dir else model_name
        file_obj = self.get_file_obj(model_file,bucket_name)
        model_obj = self.read_object(file_obj,decode=False)
        model = pickle.loads(model_obj)
        return model
    
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the specified S3 bucket."""
        try:
            # Check if folder exists by attempting to load it
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            # If folder does not exist, create it
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logging.info("Exited the create_folder method of SimpleStorageService class")
    

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        """Upload a file to S£ storage """
        self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

        #Delete the file if remove=True
        if remove:
            os.remove(from_filename)
            logging.info(f"Removed local file {from_filename} after upload")
        logging.info("Exited the upload_file method of SimpleStorageService class")

    
    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        data_frame.to_csv(local_filename,index=None,header=True)
        self.upload_file(local_filename,bucket_filename,bucket_name)


    def get_df_from_object(self, object_: object) -> DataFrame:
        content = self.read_object(object_,make_readable=True)
        df = read_csv(content,na_values="na")
        return df
    

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        csv_object = self.get_file_obj(filename,bucket_name)
        df = self.get_df_from_object(csv_object)
        return df







