from typing import Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


# ----------------------------------------------
# PREDICT ROUTE WITH PREDICTIONS VALUES RETURNED
# ----------------------------------------------


@app.get("/predict", status_code=200)
async def predict(q: Any = None):
    if not (q):
        print(q)
        raise HTTPException(status_code=400, detail="Bad request, the query is missing or invalid")
    a = {"hello": q}
    return a
