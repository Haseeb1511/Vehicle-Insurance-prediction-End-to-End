import sys
from pandas import DataFrame
from src.entity.estimator import MyModel
from src.exception import MyException
from src.logger import configure_logger
logging = configure_logger("s3_Estimator")
from src.cloud_storage.aws_storage import SimpleStorageService


class VehicleInsuranceEstimator:
    def __init__(self,bucket_name,model_path):
        self.bucket_name = bucket_name
        self.model_path =model_path
        self.s3 = SimpleStorageService()
        self.loaded_model:MyModel=None

    
    def is_model_present(self,model_path):
        return self.s3.s3_key_path_avaliable(bucket_name=self.bucket_name,s3_key=model_path)
    

    def load_model(self):
        return self.s3.load_model(model_dir=self.model_path,bucket_name=self.bucket_name)

    def save_model(self,from_file,remove:bool=False):
        return self.s3.upload_file(
            from_filename=from_file,
            to_filename=self.model_path,
            bucket_name=self.bucket_name
        )
    
    def predict(self,dataframe:DataFrame):
        if self.load_model is None:
            self.load_model = self.load_model()
        return self.loaded_model.predict(dataframe=dataframe)
    

    