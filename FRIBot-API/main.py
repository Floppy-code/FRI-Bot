from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Services.LSTMPredictionService import LSTMPredictionService

#Prediction variables
LSTMNetworkService = LSTMPredictionService('./network_short_answ_no_split_2.h5', './komplet_dataset_short_answ_backend_dictionaries', 127, 512)

#FastAPI variables
class Sentence(BaseModel):
    sentence: str

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#========== ENDPOINTS ==========
@app.get("/health")
async def get_health():
    return { "Status" : "Healthy" }

@app.post("/lstm/predict")
async def predict_sentence_lstm(request: Sentence):
    #TODO Make mock sentence work!
    return { "prediction" : LSTMNetworkService.inference(request.sentence) }

#========== ENDPOINTS ==========