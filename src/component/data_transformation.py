import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from src.constant import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from src.entity.artificat_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.logger import configure_logger
logger = configure_logger("DataTransformation")
from src.exception import MyException
from src.utils.main import save_object, save_numpy_array_data, read_yaml_file
import sys



class DataTransformation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        
    @staticmethod
    def read_data(file_path):
        return pd.read_csv(file_path)


    def get_data_transformer_obj(self):
        sc = StandardScaler()
        min_max_scaler = MinMaxScaler()

        num_feature = self._schema_config["numerical_columns"]
        mm_column = self._schema_config["mm_columns"]

        preprocess = ColumnTransformer(transformers=[(
            ("Standard Scaled",sc,num_feature),
            ("MinMax Scaler",min_max_scaler,mm_column)
        )],remainder="passthrough")

        final_pipeline = Pipeline(steps=[
            ("preprocess",preprocess)
        ])

        return final_pipeline
    
    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logger.info("Mapping 'Gender' column to binary values")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df
    

    def _create_dummy_columns(self, df):
        """Create dummy variables for categorical features."""
        logger.info("Creating dummy variables for categorical features")
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
    
    def _drop_id_column(self,df):
        """Drop id column"""
        id_column = self._schema_config["drop_columns"]
        if id_column in df.columns:
            df =df.drop(columns=id_column,axis=1)
        return df


    def initiate_data_transformation(self) :
        if not self.data_validation_artifact.validation_status:
            raise Exception(self.data_validation_artifact.message)
        
        try:
            #loading train and test data
            train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            #splitting in to x and y
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN] 
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN] 

            #Transformation on training data
            input_feature_train_df = self._map_gender_column(input_feature_train_df)
            input_feature_train_df = self._drop_id_column(input_feature_train_df)        
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)

            #Transformation on test data
            input_feature_test_df = self._map_gender_column(input_feature_test_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)        
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)

            preprocess = self.get_data_transformer_obj()

            input_feature_train_arr = preprocess.fit(input_feature_train_df)
            input_feature_test_arr = preprocess.fit(input_feature_test_df)

            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

            #concatination input and output column agter applying smote
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logger.info("feature-target concatenation done for train-test df.")

            save_object(self.data_transformation_config.transformed_object_file_path,  preprocess)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)


            return DataTransformationArtifact(
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
        except Exception as e:
            raise MyException(e,sys) from e

