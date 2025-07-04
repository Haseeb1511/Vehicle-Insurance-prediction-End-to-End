from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artificat_entity import DataIngestionArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from sklearn.metrics import f1_score
from src.exception import MyException
from src.logger import configure_logger
logger = configure_logger("model_evaluation")
from src.constant import TARGET_COLUMN,SCHEMA_FILE_PATH
from src.utils.main import load_object
import os,sys
import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.utils.main import read_yaml_file
from src.entity.s3_estimator import VehicleInsuranceEstimator
from dataclasses import dataclass


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float

class ModelEvaluation:
     
    def __init__(self,model_eval_config:ModelEvaluationConfig,data_ingestion_artifact:DataIngestionArtifact,
        model_trainer_artifact:ModelTrainerArtifact):

        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

    def get_best_model(self):
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path=self.model_eval_config.s3_model_key_path
            estimator = VehicleInsuranceEstimator(bucket_name=bucket_name,
                                               model_path=model_path)

            if estimator.is_model_present(model_path=model_path):
                return estimator
            return None

        except Exception as e:
            raise  MyException(e,sys)

    
    
    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df

    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
        df = pd.get_dummies(df, drop_first=True)
        return df
    
    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logger.info("Renaming specific columns and casting to int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df
    
    def _drop_id_column(self, df):
        """Drop the 'id' column if it exists."""
        logger.info("Dropping 'id' column")
        if "_id" in df.columns:
            df = df.drop("_id", axis=1)
        return df
    
    #--------------Preprocessing completed----------------------------------

    def evaluate_model(self)->EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x = test_df.drop(TARGET_COLUMN,axis=1)  #input
            y = test_df[TARGET_COLUMN]  #output

            x = self._map_gender_column(x)
            x = self._drop_id_column(x)
            x = self._create_dummy_columns(x)
            x = self._rename_columns(x)

            trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path)

            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            trained_model_accuracy = self.model_trainer_artifact.metric_artifact.accuracy
            logger.info(f"Acuracy = {trained_model_accuracy} and f1_Score {trained_model_f1_score}")

            best_model_f1_score = None
            best_model = self.get_best_model()

            if best_model is not None:
                logger.info(f"Computing F1_Score for production model..")
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)
                logger.info(f"F1_Score-Production Model: {best_model_f1_score}, F1_Score-New Trained Model: {trained_model_f1_score}")

            temp_model_best_score_f1 = 0 if best_model_f1_score is None else best_model_f1_score

            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > temp_model_best_score_f1,
                difference=trained_model_f1_score- temp_model_best_score_f1
            )

            return result
        except Exception as e:
            raise MyException(e, sys) 
    
    
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            evaluat_model = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluat_model.is_model_accepted,
                changed_accuracy=evaluat_model.difference,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path
            )
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys) from e


