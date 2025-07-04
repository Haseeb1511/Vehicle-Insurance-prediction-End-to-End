from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
from typing import List,Literal,Annotated
from src.pipeline.prediction_pipline import VehicleData,VehicleDataClassifier

app = FastAPI()

class VehicleDataRequest(BaseModel):
    Gender: str
    Age: int
    Driving_License: int
    Region_Code: float
    Previously_Insured: int
    Annual_Premium: float
    Policy_Sales_Channel: float
    Vintage: int
    Vehicle_Age_lt_1_Year: int
    Vehicle_Age_gt_2_Years: int
    Vehicle_Damage_Yes: int

@app.post("/pred")
def main(data:VehicleDataRequest):
    try:
        vehicle_data = VehicleData(
                Gender=data.Gender,
                Age=data.Age,
                Driving_License=data.Driving_License,
                Region_Code=data.Region_Code,
                Previously_Insured=data.Previously_Insured,
                Annual_Premium=data.Annual_Premium,
                Policy_Sales_Channel=data.Policy_Sales_Channel,
                Vintage=data.Vintage,
                Vehicle_Age_lt_1_Year=data.Vehicle_Age_lt_1_Year,
                Vehicle_Age_gt_2_Years=data.Vehicle_Age_gt_2_Years,
                Vehicle_Damage_Yes=data.Vehicle_Damage_Yes
            )
        
        # Converting the input to Dataframe
        inpur_df = vehicle_data.get_vehicle_input_data_frame()

        classifier = VehicleDataClassifier()

        pred = classifier.predict(inpur_df)

        return {"Prediction":pred}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


#uvicorn app:app --reload