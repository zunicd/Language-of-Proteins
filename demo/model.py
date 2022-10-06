# Import dependencies
from pathlib import Path
import joblib
import os
import numpy as np
import h5py
import subprocess

BASE_DIR = Path(__file__).resolve(strict=True).parent

# Create fasta file
def create_temp_fa(embedding):
    path_fa = Path(BASE_DIR).joinpath("temp_fa.fa")
    Seq = {}
    Seq['header'] = embedding
    with open(path_fa, 'w') as fout:
        for header, sequence in Seq.items():
            fout.write(f">{header}\n{sequence}\n")
    return path_fa

# Get model details
def model_details(task):
    models_dir = Path(BASE_DIR.parent).joinpath('saved_models/best_models')
    for file in os.listdir(models_dir):
        if file.startswith(task):
            model_name  = file

    model_file = Path(BASE_DIR).joinpath(models_dir, model_name)
    pool = model_name.split('_')[2]
    pt_model =  f"prose_{model_name.split('_')[1]}"
    return pt_model, pool, model_file

# Calculate embeddings
def embed(path_fa, pt_model, pool):
    ## model = 'prose_dlm'
    ## pool = 'avg'
    path_h5 = Path(BASE_DIR).joinpath(f"temp_h5.h5")
    subprocess.run(["python", "../prose/embed_sequences.py", "--model", f"{pt_model}", "--pool", f"{pool}", "-o", f"{path_h5}", f"{path_fa}"], check=True)

   # Read embeddings from h5 file    
    with h5py.File(path_h5, 'r') as hf:
        for key in hf.keys():
            X = np.array(hf.get(key)).reshape(1, -1)  
    # Remove the temporary files
    path_fa.unlink()   
    path_h5.unlink()   
    return X

# Load saved model and predict on new data
def predict(X, model_file):
    if not model_file.exists():
        return False
    model = joblib.load(model_file)  
    prediction = model.predict(X)
    return prediction

# Output a dictionary of prediction
def convert(prediction, task):
    if prediction == 0:
        return f"non-{task.upper()}"
    else: 
        return f"{task.upper()}"
