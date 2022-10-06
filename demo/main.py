# Import dependencies
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, ValidationError, validate_arguments, BaseConfig
from model import create_temp_fa, model_details, embed, predict, convert
import numpy as np

app = FastAPI()

# pydantic models
class ProteinIn(BaseModel):
    task : str
    protein: str

class ProteinOut(ProteinIn):
    prediction: str

# /predict endpoint
@app.post("/predict", response_model=ProteinOut, status_code=200)
def get_prediction(payload: ProteinIn):
    task_in = payload.task.lower()
    protein = payload.protein

    # Check if task is valid
    valid_tasks = ['acp', 'amp', 'dbp', 'dna_binding']
    if task_in not in valid_tasks:
        raise HTTPException(status_code=400, detail="Task not available")

    if task_in == 'dna_binding':
        task = 'dbp'
    else:
        task = task_in

    # Create temporary fasta file
    path_fa = create_temp_fa(protein)

    # Get model details
    pt_model, pool, model_file = model_details(task)

    # Embed the protein
    embedding = embed(path_fa, pt_model, pool)

    # Predict the protein
    prediction = predict(embedding, model_file)

    response_object = {
        "task": task_in,
        "protein": protein,
        "prediction": convert(prediction, task)
    }
    return response_object
