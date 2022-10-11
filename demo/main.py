# Import dependencies
from fastapi import FastAPI, Query, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from model import create_temp_fa, model_details, embed, predict, convert

app = FastAPI()

# Add static files and Jinja templates
staticfiles = StaticFiles(directory="./static")
app.mount("/static", staticfiles, name="static")
templates = Jinja2Templates(directory="templates")

# root endpoint
@app.get('/')
def root():
    return 'Welcome to Protein Language API'

# /predict endpoint
@app.get('/predict')
def form_post(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.post("/predict", response_class=HTMLResponse, status_code=200)
def get_prediction(request:Request, task: str = Form(...), protein: str = Form(...)):

    # Create temporary fasta file
    path_fa = create_temp_fa(protein)

    # Get model details
    pt_model, pool, model_file = model_details(task)

    # Embed the protein
    embedding = embed(path_fa, pt_model, pool)

    # Predict the protein
    prediction = predict(embedding, model_file)

    # Tasks description dictionary
    tasks_d = {}
    tasks_d['acp'] = 'Anticancer Peptides (ACP)'
    tasks_d['amp'] = 'Antimicrobial Peptides (AMP)'
    tasks_d['dbp'] = 'DNA-Binding Proteins (DBP)'

    # Get prediction
    prediction = convert(prediction, task)

    # Prepare context dictionary
    task = tasks_d[task]
    text1 = f"Running {task} prediction:"
    
    context={
        'request': request, 
        'prediction': prediction, 
        'task':task, 
        'protein':protein, 
        'text1':text1
        }
    # Send the context dictionary to the Jinja template
    return templates.TemplateResponse('index.html', context=context)