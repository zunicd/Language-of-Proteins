## Baseline Models
For each of our classification tasks, we investigated two baseline models
1. Bag of Words (BoW) was used for sequence embedding, followed by a simple Neural Network which was used for binary classification
2. [Sequence Graph Transform (SGT)](https://github.com/cran2367/sgt) was used for sequence embedding, followed by a Neural Network with the same architecture as the BoW method for binary classification

Results are summarized below (Accuracy):
| Embedding   | Model         | ACP  |AMP   |DBP   |
| ----------- |:-------------:|-----:|-----:|-----:|
| BoW         | NN            | 68.1 |90.6  |79.1  |
| SGT         | NN            | 70.9 |82.5  |71.5  |

The BoW does not retain any sequence information. SGT uses the sequence information, but is not pre-trained on any protein data (it can handle any sequence data from scratch). It was rather surprising to see BoW do nearly as well (for ACP) or even better (for AMP and DBP).