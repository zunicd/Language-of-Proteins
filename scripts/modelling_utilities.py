# Collection of modelling utilities
import os
import pandas as pd
import joblib

from sklearn.model_selection import GridSearchCV, StratifiedKFold

# Classification metrics
from sklearn.metrics import accuracy_score, f1_score
random_state = 10


# Function to get embedding folders and fasta files for the task
def get_emb_folders(task, data_folder='../../data'):

    # Defune base folder
    base = os.path.join(data_folder, task)
    
    paths_test, test_fa = [], []
    paths_train, train_fa = [], []
    paths_all, all_fa = [], []
    for root, dirs, files in os.walk(base, topdown=False):
        #print(root)
        tail = os.path.split(root)[1]
        if tail not in ['esm', 'prose', 'test', 'train', 'all_data']:
            if 'test' in root:
                paths_test.append(root)
            elif 'train' in root:
                paths_train.append(root)
            elif 'all' in root:
                paths_all.append(root)
    
    # Last folder in a loop is the "base"
    for file in files:
        if 'fa' in file:
            if 'test' in file:
                test_fa.append(os.path.join(base, file))
            elif 'train' in file:
                train_fa.append(os.path.join(base, file))
            else:
                all_fa.append(os.path.join(base, file))
            
    
    if len(paths_all) != 0:
        return paths_all, all_fa
    else:
        fastas = list(zip(train_fa, test_fa))
        paths = list(zip(paths_train, paths_test))
        return paths, fastas
    
# ===============
    
# Fit, hypertune and save models
def fit_tune_CV(pipe, hyper_params, scorer, path_pt, X_train, y_train, task):
        
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    # Create empty dictionary called fitted_models
    fit_models = {}
   
    # Loop through model pipelines, tuning each one and saving it to fitted_models
    for name, pipeline in pipe.items():
        # Create cross-validation object from pipeline and hyperparameters
        grid = GridSearchCV(pipeline, hyper_params[name], cv=skf,
                             scoring=scorer, n_jobs=4)

        # Fit model on X_train, y_train
        grid.fit(X_train, y_train)
        
        # Creating names
        tail = os.path.split(path_pt)[1].split('_')
        tail.pop(1)
        model_name = f'{"_".join(tail)}_{name}'
        model_file = f'{model_name}.sav'
        model_path = os.path.join('../../saved_models', task, model_file)
        model = model_name.split('_', 1)[1]
        # Store model into dictionary fit_models
        fit_models[model] = grid
        # Save model
        joblib.dump(grid, model_path)
        # Print '{model} has been fitted and saved'
        print(model, 'has been fitted and saved')
    return fit_models

# =============

# Evaluate models
def evaluation(fit_models, X_test, y_test):
    lst = []
    for name, model in fit_models.items():
        # Get predictions
        y_pred = model.predict(X_test)
        # Get cv best score and calculate f1_score and accuracy
        lst.append([name, model.best_score_, f1_score(y_test, y_pred, average='macro'),
                    accuracy_score(y_test, y_pred)])
    # Create evaluation dataframe
    eval_df = pd.DataFrame(lst, columns=['model', 'cv_best_score', 'f1_macro', 'accuracy'])
    eval_df.set_index('model', inplace = True)
    return eval_df

