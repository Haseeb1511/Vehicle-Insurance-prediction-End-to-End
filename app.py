#In your FastAPI code, request: Request is a function parameter that tells FastAPI to inject the HTTP request object into your endpoint or class
from fastapi import FastAPI,HTTPException,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
import os,sys

# Importing Local Modules
from src.pipeline.prediction_pipline import VehicleData,VehicleDataClassifier
from src.pipeline.training_pipeline import TrainPipeline
from src.exception import MyException


app = FastAPI()

# ---->> When your FastAPI backend is separate from your frontend (e.g., React, Streamlit, or a mobile app we use CORSMiddleware
# Configure middleware to handle CORS, allowing requests from any origin
# Cross origin resource sharing(CIRS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # ← Allow ANY origin (public)
    allow_credentials=True,      # ← Allow cookies, auth headers
    allow_methods=["*"],         # ← Allow ALL HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],         # ← Allow ALL custom headers
)

# Mount the 'static' directory for serving static files (like CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")

class DataFrame:
    """This function get data from user"""
    def __init__(self,request:Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    
    async def get_vehicle_data(self):
        """This function get data from the HTML(form)"""
        form  = await self.request.form()
        self.Gender = form.get("Gender")
        self.Age = form.get("Age")
        self.Driving_License = form.get("Driving_License")
        self.Region_Code = form.get("Region_Code")
        self.Previously_Insured = form.get("Previously_Insured")
        self.Annual_Premium = form.get("Annual_Premium")
        self.Policy_Sales_Channel = form.get("Policy_Sales_Channel")
        self.Vintage = form.get("Vintage")
        self.Vehicle_Age_lt_1_Year = form.get("Vehicle_Age_lt_1_Year")
        self.Vehicle_Age_gt_2_Years = form.get("Vehicle_Age_gt_2_Years")
        self.Vehicle_Damage_Yes = form.get("Vehicle_Damage_Yes")

    
@app.get("/",tags=["authentication"])
async def index(request:Request):
    return template.TemplateResponse(
        "vehicledata.html",{"request":request,
                            "context":"Rendering"}
    )



@app.get("/train")
async def trainRouteClient():
    """This endpoint train the model"""
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return "Training Successful"
    except Exception as e :
        raise MyException(e,sys) from e


@app.post("/")
async def predRouteClient(request:Request):
    """This endpoint predict base on user input"""
    try:
        form = DataFrame(request)
        await form.get_vehicle_data()
        vehicle_data = VehicleData(
                                Gender= form.Gender,
                                Age = form.Age,
                                Driving_License = form.Driving_License,
                                Region_Code = form.Region_Code,
                                Previously_Insured = form.Previously_Insured,
                                Annual_Premium = form.Annual_Premium,
                                Policy_Sales_Channel = form.Policy_Sales_Channel,
                                Vintage = form.Vintage,
                                Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
                                Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
                                Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
        )

        # Convert form data into a DataFrame for the model
        df = vehicle_data.get_vehicle_input_data_frame()

         # Initialize the prediction pipelin
        model_predict = VehicleDataClassifier()

        value = model_predict.predict(dataframe=df)[0]

        # Interpret the prediction result as 'Response-Yes' or 'Response-No'
        status = "Response-Yes" if value == 1 else "Response-No"

        return template.TemplateResponse(
            "vehicledata.html",
            {"request":request,"context":status}
        )
    except Exception as e:
        raise MyException(e,sys) from e
    

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=5000)


#Cross-Origin Resource Sharing (CORS)

# Original: Allow all origins for Cross-Origin Resource Sharing (CORS) Configure middleware to handle CORS, allowing requests 
# from any origin.
# Simplified: When you load a web app (e.g., from http://localhost:3000) and it tries to access a server (e.g., http://localhost:8000), 
# CORS controls whether the browser allows this connection. By default, browsers block requests from one 
# "origin" (like a domain or port) to another for security reasons.
# In this code, allow_origins=["*"] is set, which means allow all origins (any domain or app can connect). The middleware 
# is added so that your FastAPI app accepts requests from any origin, making it easier for you to access the API from anywhere, 
# such as different frontend apps.