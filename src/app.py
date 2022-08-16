from typing import Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


# ----------------------------------------------
# PREDICT ROUTE WITH PREDICTIONS VALUES RETURNED
# ----------------------------------------------


@app.get("/predict", status_code=200)
async def predict(q: Optional[Any] = None):
    if not (q):
        raise HTTPException(status_code=400, detail="Bad request, the query is missing or invalid")
    prediction = {"hello": q}
    return prediction

# if __name__ == '__main__':
#     port = os.getenv('PORT', default=8000)
#     config = uvicorn.Config("app:app", host='0.0.0.0', port=port, reload=True)
#     server = uvicorn.Server(config)
#     server.run()
