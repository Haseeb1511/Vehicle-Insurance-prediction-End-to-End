from src.cloud_storage.aws_storage import SimpleStorageService
from src.logger import configure_logger
logger = configure_logger("model_pusher")
from src.exception import MyException
from src.entity.artificat_entity import ModelPusherArtifact,ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import VehicleInsuranceEstimator
import sys,os
class ModelPusher:

    def __init__(self,model_pusher_config:ModelPusherConfig,model_eval_artifact:ModelEvaluationArtifact):
        self.model_eval_artifact = model_eval_artifact
        self.model_pusher_config = model_pusher_config
        self.s3 = SimpleStorageService()
        self.vehicle_insurance_estimator = VehicleInsuranceEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )

    def initiate_model_pusher(self):
        try:
            self.vehicle_insurance_estimator.save_model(from_file=self.model_eval_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path
            )
            logger.info("Uploaded artifacts folder to s3 bucket")
            logger.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logger.info("Exited initiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys) from e