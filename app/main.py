from json import load
from fastapi import FastAPI,  Query, Request
from fastapi.responses import JSONResponse
from joblib import load
import os
import pandas as pd
from typing import Union

import xgboost

from . import models


MODEL_PATH_ENV_VAR = 'MODEL_PATH'

'''
    The method creates webv app and serves the requests
'''
def create_app():
    
    model = None
    
    #setup app metada    
    tags_metadata = [
        {
            "name": "uci",
            "description": "Serving for UCI Hart Diseases model",
        }
    ]
    #create the app
    app = FastAPI(
        title="UCI Hart Deseases Predict",
        description="Serving for UCI Hart Diseases model",
        version="0.1.0",
        openapi_tags=tags_metadata,
        docs_url="/",
        redoc_url=None,
    )

    @app.on_event("startup")
    async def startup():
        nonlocal model
        model_path = os.getenv(MODEL_PATH_ENV_VAR)
        if not os.path.exists(model_path):
            raise Exception(f"The model is not found at specified path {model_path}")
        #laod the model with joblib
        model = load(model_path)
    
    @app.on_event("shutdown")
    async def shutdown():
        # cleanup
        pass
    
    @app.middleware("http")
    async def model_session_middleware(request: Request, call_next):
        #we can simply copy the model pointer as XGBoost allows parallel predicts
        request.state.model = model
        response = await call_next(request)
        return response
    
    
    '''
        Predict method, accept get parameters from Request, validate, encode and get response from the model
    '''
    @app.get("/predict", 
        operation_id="predict",
        tags=["predict"], 
        description="This method returns the model predictions",
        response_model = models.HartDiseaseModelResponse,
        responses={
            200: {
                "description": "Model predict for passed data",
                "content": {
                    "application/json": {
                        "example": {"prediction": 3}
                        }
                    }
                }
            }
        )
    async def predict(
        request:Request,
        age: int = Query(title="Age of the patient", gt = 0), 
        sex: Union[str, None] = Query(default=None, title="Sex of the patient"), 
        dataset: Union[str, None] = Query(default=None, title="Geo location of the patient"), 
        cp: Union[str, None] = Query(default=None, title="Chest pain type of the patient"), 
        trestbps: Union[float, None] = Query(default=None, title="Resting blood pressure of the patient", gt = 0), 
        chol: Union[float, None] = Query(default=None, title="Serum cholesterol in mg/dl of the patient", gt = 0), 
        fbs: Union[bool, None] = Query(default=None, title="If fasting blood sugar > 120 mg/dl"), 
        restecg: Union[str, None] = Query(default=None, title="Resting electrocardiographic results of the patient"), 
        thalch: Union[float, None] = Query(default=None, title="Maximum heart rate achieved of the patient", gt = 0), 
        exang: Union[bool, None] = Query(default=None, title="Exercise-induced angina of the patient"), 
        oldpeak: Union[float, None] = Query(default=None, title="ST depression induced by exercise relative to rest", ge = 0), 
        slope: Union[str, None] = Query(default=None, title="The slope of the peak exercise ST segment of the patient"), 
        ca: Union[float, None] = Query(default=None, title="The number of major vessels of the patient", ge=0, le=3), 
        thal: Union[str, None] = Query(default=None, title="Thal of the patient")
    ) -> JSONResponse:
        #create the request for saved model
        df = pd.DataFrame([[age, sex, dataset, cp, trestbps, chol, fbs, restecg, thalch, exang, oldpeak, slope, ca, thal]], 
                          columns=['age','sex', 'dataset','cp','trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak' ,'slope','ca', 'thal'],
        )
        #perform the predict        
        class_id = request.state.model.predict(df)
        return {"prediction":class_id}
    
    return app
    #end of create_app

#entry point
app = create_app()