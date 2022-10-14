# Modelling

We used the previously computed embeddings as input to our models. 

For each classification task there were 8 combinations, as shown in the table below.

|       | Number of pre-trained  models | Pooling operations |
| ----- | ---------------------- | ------------------- |
| ESM   | 2                      | 1                   |
| ProSE | 2                      | 3                   |

We used 4 machine learning algorithms:

- SVM
- XGBoost
- Random Forest
- Logistic Regression

All the different combinations of pre-trained and classification models resulted in 32 `pipelines` for each classification task.

## Modelling Pipeline

The image below displays the pipeline we used in this project.

<img src="images/pipeline_hp-tuning.png" style="zoom:80%;" />

## Modelling Loop

For each task we were following the same experimentational setup that includes the following steps:

1. Loop through train and test embedding folders
2. Run the function `read_embeddings()` for train embeddings to get `X_train` and `y_train`
3. Run the function `read_embeddings()` for test embeddings to get `X_test` and `y_test`
4. Define and print the output header
5. Use the function `fit_tune_CV()`to to do the following:
   - use the above defined `pipelines` and `hyperparameter` dictionaries and `GridSearchCV()` to train models
   - save the models with `joblib`
   - create a dictionary of the models for each set of embedding folders
6. Run the function `evaluation()` to create an evaluation dataframe for each set of embedding folders

For "AMP" the first three steps are slightly different:
1. Loop through embedding folders
2. Run the function `read_embeddings()` for all_data embeddings to get `X` and `y`
3. Split `X` and `y` into train and test sets

## Results

### Best Performing Models

For each task we created a dataframe with results for all 32 models and sorted them by accuracy. In the table below we listed the best performing models for each classification task.

| Task | Best performing model | Accuracy | f1_macro |
| ---- | --------------------- | --------------- | --------------- |
| ACP | dlm\_avg\_svm         | 0.75            | 0.75          |
| AMP | mt\_avg\_lr           | 0.94            | 0.94         |
| DBP | dlm\_max\_rf          | 0.88            | 0.88           |

The difference between the best and worst performing models was 6-8%.

Because the datasets are well balanced, accuracy and f1_macro are pretty much the same.

### Top 10 Performing Pipelines

We analyzed top 10 performing `pipelines` for each class and collected data in the table below:

| Task | Data Size (train, test) | dlm  | mt   | esm1b | esm1v | avg  | max  | sum  | xgb  | svm  | lr   | rf   |
| ---- | ----------------------- | ---- | ---- | ----- | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ACP  | 1300, 300               | 4    | 4    | 1     | 1     | 6    | 1    | 3    | 2    | 5    | 3    | NaN  |
| AMP  | 3000, 1000              | 3    | 5    | NaN   | 2     | 6    | 2    | 2    | Nan  | 5    | 5    | NaN  |
| DBP  | 14000, 2200             | 5    | 3    | 1     | 1     | 5    | 3    | 2    | 6    | 2    | NaN  | 2    |

Some conclusions from this table:

- `ProSE` pretrained models outperform `ESM`, `“dlm”` and `“mt”` `ProSE` models are pretty equal.

- Overall best performance is with `“avg”` pooling.

- `SVM` is the best universal performer.

- `XGBoost` is best for bigger datasets, Logistic Regression for smaller datasets.

- `Random Forest` performs well for “DBP” only.

  




