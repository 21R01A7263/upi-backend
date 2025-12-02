from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import List
app=FastAPI()






@app.get("/")
def root():
    return {"message": "Hello World"}
print("Running on http://localhost:8000/")

        