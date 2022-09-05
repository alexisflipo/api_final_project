from typing import Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
import pandas as pd
import pickle
import os
# ----------------------------------------------
# INSTANCIATE FastAPI Class
# ----------------------------------------------

app = FastAPI()

# ----------------------------------------------------
# ALLOW LIST OF ORIGINS TO LMAKE CROSS-ORIGIN REQUESTS
# ----------------------------------------------------

origins = ["http://localhost:8000/", "http://localhost:8000/predict"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------
# GET INDEX ROUTE
# ----------------------------------------------

def open_binaries_model():
    with open('src/ml_scripts/models/lasso_model.sav', 'rb') as f:
        model = pickle.load(f)
    return model

@app.get("/")
def redirect_docs():
    return RedirectResponse('http://localhost:8000/docs')


# ----------------------------------------------
# PREDICT ROUTE WITH PREDICTIONS VALUES RETURNED
# ----------------------------------------------

@app.get("/predict", status_code=200)
async def predict(country:str, remote_ratio: int, xp_encoded:int, company_size:int):
    model = open_binaries_model()
    if not country:
        raise HTTPException(status_code=400, detail="Bad request, the query is missing or invalid")
    else:
        country = str(country).lower()
        default_values = { 'europe': 0.0, 'america': 0.0, 'asia': 0.0, 'remote_ratio': None, 'xp_encoded': None, 'company_size_encoded': None }
        default_values.update({'xp_encoded' : int(xp_encoded), "company_size_encoded": int(company_size), country: 1.0, 'remote_ratio': int(remote_ratio)})
        default_values = [default_values]
        pred_df = pd.DataFrame(default_values)
        predictions = {'Salary predictions in $USD' : round(model.predict(pred_df).tolist()[0] * 1000, 1)}
    
    return predictions
