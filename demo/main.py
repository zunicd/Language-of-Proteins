# Import dependencies
from fastapi import FastAPI, Query, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError, validate_arguments, BaseConfig
from model import create_temp_fa, model_details, embed, predict, convert
import numpy as np

app = FastAPI()
# staticfiles = StaticFiles(directory="static")
# app.mount("/static", staticfiles, name="static")
templates = Jinja2Templates(directory="templates")



@app.get('/')
def root():
    return 'Welcome to Protein Language API'

# pydantic models
class ProteinIn(BaseModel):
    task : str
    protein: str

class ProteinOut(ProteinIn):
    prediction: str

# /predict endpoint
@app.get('/predict')
def form_post(request: Request):
    ## result = ''
    return templates.TemplateResponse('index.html', context={'request': request})

@app.post("/predict", response_model=ProteinOut, status_code=200)
# def get_prediction(payload: ProteinIn, request:Request):
def get_prediction(request:Request, task: str = Form(...), protein: str = Form(...)):
    # task_in = payload.task.lower()
    # protein = payload.protein
    task_in = task.lower()
    #protein = payload.protein

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

    # response_object = {
    #     "task": task_in,
    #     "protein": protein,
    #     "prediction": convert(prediction, task)
    # }

    tasks_d = {}
    tasks_d['acp'] = 'Anticancer Peptides (ACP)'
    tasks_d['amp'] = 'Antimicrobial Peptides (AMP)'
    tasks_d['dbp'] = 'DNA-Binding Proteins (DBP)'

    prediction = convert(prediction, task)

    task = tasks_d[task]
    text1 = f"Running {task} prediction:"
    #return response_object
    return templates.TemplateResponse('index.html', context={'request': request, 'prediction': prediction, 'task':task, 'protein':protein, 'text1':text1})
