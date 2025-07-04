import sys
import os
from src.logger import configure_logger
logger = configure_logger("ModelTrainning")
from src.exception import MyException
from src.entity.artificat_entity import ModelTrainerArtifact,DataTransformationArtifact,ClassificationMetricArtifact,DataTransformationArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.main import load_numpy_array_data, load_object, save_object
from typing import Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from src.entity.estimator import MyModel



class ModelTrainer:

    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_obj_and_report(self,train:np.ndarray,test:np.ndarray):
        try:
            x_train,y_train,x_test,y_test = train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            
            model = RandomForestClassifier(n_estimators=self.model_trainer_config._n_estimators,
                                        max_depth=self.model_trainer_config._max_depth,
                                        min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                                        min_samples_split=self.model_trainer_config._min_samples_split,
                                        criterion=self.model_trainer_config._criterion,
                                        random_state=self.model_trainer_config._random_state
                                        )
            logger.info(f"Model selected is {model}")
            logger.info("model training started ......")
            model.fit(x_train,y_train)

            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test,y_pred)
            percision  = precision_score(y_test, y_pred, average='binary')
            f1score = f1_score(y_test, y_pred, average='binary')
            recall = recall_score(y_test, y_pred, average='binary')
            logger.info(f"Model training finished with accuracy of : {accuracy}")
            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1score,
                precision_score=percision,
                recall_score=recall,
                accuracy=accuracy
            )
            return model,metric_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_array = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_array = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            trained_model,metric_artifact = self.get_model_obj_and_report(train=train_array,test=test_array)
            
            # Load preprocessing object
            preprocess_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)  #loading the preprocessing pipline

            # if metric_artifact.accuracy < self.model_trainer_config.expected_accuracy:
            #     raise Exception("No model found with score above the base score")
            if accuracy_score(train_array[:, -1], trained_model.predict(train_array[:, :-1])) < self.model_trainer_config.expected_accuracy:
                raise Exception("No model found with score above the base score")
            
            my_model = MyModel(preprocessing_object=preprocess_obj,trained_model_object=trained_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=my_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )

            return model_trainer_artifact
        
        except Exception as e:
            raise MyException(e,sys) from e