# Collection of modelling utilities:
#    get_emb_folders - prepare paths to embedding folders and fasta files for the given task
#    fit_tune_CV - tune hyperparameters using GridSearchCV, fit and save models
#    evaluation - evaluate models and store results into a dataframe

# Import dependencies
import os
import pandas as pd
import joblib
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score
random_state = 10

# Function to prepare paths to embedding folders and fasta files for the given task
def get_emb_folders(task, data_folder='../../data'):
    """ Prepare paths for embedding folders and fasta files

    Args:
        task: protein group - ['acp', 'amp', 'dna_binding']
        data_folder: root of data folder - ['../../data'] default

    Returns:
        paths: paths to embedding folders; for 'acp,', 'dna_binding'
            or
        paths_all: paths to embedding folders; for 'amp'
        fastas: paths to fasta files;  for 'acp,', 'dna_binding'
            or
        all_fa: paths to fasta files; for 'amp'
    """
    # Define base folder
    base = os.path.join(data_folder, task)
    # Initialize lists
    paths_test, test_fa = [], []
    paths_train, train_fa = [], []
    paths_all, all_fa = [], []
    
    # Prepare embedding folders
    for root, dirs, files in os.walk(base, topdown=False):
        # Skip root folders with a tail in the list below
        tail = os.path.split(root)[1]
        if tail not in ['esm', 'prose', 'test', 'train', 'all_data']:
            # Separate folders with 'test', 'train' or 'all' in root
            if 'test' in root:
                paths_test.append(root)
            elif 'train' in root:
                paths_train.append(root)
            elif 'all' in root:
                paths_all.append(root)
    
    # Prepare fasta files
    # The last root folder in the above loop is the "base"
    # Iterate through files in the "base" and list fasta file paths
    for file in files:
        # Look for fasta files (.fa extension)
        if 'fa' in file:
            # Separate files with 'test', 'train' or 'all' in file path
            if 'test' in file:
                test_fa.append(os.path.join(base, file))
            elif 'train' in file:
                train_fa.append(os.path.join(base, file))
            else:
                all_fa.append(os.path.join(base, file))
            
    # For 'amp' task return paths_all and all_fa
    if len(paths_all) != 0:
        return paths_all, all_fa
    else:
        # return lists of tuples of (train, test) paths
        fastas = list(zip(train_fa, test_fa))
        paths = list(zip(paths_train, paths_test))
        return paths, fastas
    
# ===============
    
# Function to tune hyperparameters using GridSearchCV, fit and save models
def fit_tune_CV(pipe, hyper_params, scorer, path_pt, X_train, y_train, task):
    """ Tune hyperparameters using GridSearchCV, fit and save models

    Args:
        pipe: dictionary of model pipelines
        hyper_params: dictionary of hyperparameter grids
        scorer: metrics to evaluate the performance of the cross-validated model 
        path_pt: path to embedding folders, used to create names of the models
        X_train: features - train embedding vectors
        y_train: train target variables
        task: protein group - ['acp', 'amp', 'dna_binding'],
              used to name folders for saving models

    Returns:
        fit_models: dictionary of fitted models 
    """ 
    # Made folds by preserving the percentage of samples for each class
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    # Create empty dictionary called fit_models
    fit_models = {}
   
    # Loop through model pipelines, tuning each one and saving it to fit_models
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

# Function to evaluate models and store results into a dataframe
def evaluation(fit_models, X_test, y_test):
    """ Evaluate models and store results into a dataframe

    Args:
        fit_models: dictionary of fitted models
        X_test: test embedding vectors
        y_train: test target variables

    Returns:
        eval_df: dictionary of evaluation dataframes
    """ 
    lst = []
    # Iterate through models in 'fit_models'
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

