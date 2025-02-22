# Language of Proteins

FourthBrain Capstone: **Learning the Language of Proteins** (InstaDeep Industry Project)

Group Members: Damir Zunic, Michal Roztocki, and Tikeswar Naik

Our full presentation deck can be found [here](https://docs.google.com/presentation/d/1no5DAa89q0E3RuRHps87ZcibQ7QjYcO0r0hgj_1juh8/edit?usp=sharing).

## Background

Drug development and discovery is a time and labor intensive process that has the potential to be enhanced and improved by next-generation protein sequencing techniques.

Recent breakthroughs in Natural Language Processing (NLP) and training of large transformer models have paved the way for new types of domain-specific deep language models. In the biological domain, development of general-purpose protein language models that are capable of predicting specific protein types could, among other things, pave the way to more effective, safer cancer treatments.

## Tasks
A protein can be represented by a sequence of tokens where each token is an amino acid (e.g., GMASKAGSVLGKITKIALGAL). Peptides are proteins of relatively small lengths.

We have three datasets from InstaDeep, one for each of the following types of proteins:
1. Anticancer Peptides (ACP)
2. Antimicrobial Peptides (AMP)
3. DNA-Binding Proteins (DBP)

For each of these datasets, we will develop a system that can predict, given a sequence of amino acids, if a peptide is an ACP, AMP, or DBP.

## Data
During our project, the data was stored in a `data` directory in the root folder, although we did not have permission to share it in this repo. The data is in the form of a set of train and test CSV files with the following columns:
1. `sequence`: the sequence of amino acids
2. `label`: the label for the sequence (e.g., ACP, AMP, or DBP)

## Data Lineage
The data was obtained from the following sources:
1. ACP: Instadeep
2. AMP: Instadeep
3. DBP: Instadeep, via https://github.com/hfuulgb/PDB-Fusion/tree/main/DNA

## Evaluation
We evaluated our models using the following metrics:
1. Accuracy
2. F1 Score

## Models
We used the following pre-trained protein language models to get embeddings for our sequences:
1. [ProSE](https://github.com/tbepler/prose) (Protein Sequence Embeddings)
2. [ESM](https://github.com/facebookresearch/esm) (Evolutionary Scale Modeling)

We then tested a variety of classical ML and deep learning models on the embeddings to predict the labels for the sequences.

For more details on the embedding procedure, check the [readme](https://github.com/zunicd/Language-of-Proteins/tree/main/notebooks/embeddings) in the embeddings subfolder.

## Results
We reported the results of our modelling in the `results` directory, after which we settled on a pipeline for each task for deployment.

## Deployment
We deployed our models using FastAPI and an html template. We containerized the app using Docker and deployed it on AWS using an EC2 instance. To run the app yourself locally, you can use the following commands if you have Docker installed:

```
docker pull zunicd/damirz_repo:proteins-2
docker run -d --name proteins_cont -p 8000:80 IMAGE_ID
```
Note: IMAGE_ID is the ID of the image you just pulled. You can find it by running the command `docker images` and copying the ID of the image with the name `zunicd/damirz_repo:proteins-2`.

You can then access the app at `http://localhost:8000/predict`. Pick the classification task you want to run and enter a sequence of amino acids. The app will then return the predicted label for the sequence.

Alternatively, you can follow the steps in the `Steps to deploy on AWS` text file in this root folder to deploy the app remotely. 

For more details, check the [readme](https://github.com/zunicd/Language-of-Proteins/tree/main/demo) in the demo subfolder.

## Limitations

Some of the limitations of our project include:
1. Our data was perfectly balanced for each classification task, which is almost certainly not representative of the actual appearance frequency of each of these peptides. We did not address this issue, as we were unable to ascertain the actual distribution for each type of protein in the expected space of proteins, if that is even possible. This could lead to a bias in our predictions, and as such should be addressed in future work.
2. We did not look for any extra examples of ACP, AMP, and DBP data to supplement the data from InstaDeep, nor were we able to get in contact with the company to discuss whether the data we received was representative of the data we should expect in production. It is therefore possible that our models will not generalize well to new data. This will require monitoring in production to ensure that the models are performing as expected.
3. Currently, our deployment is only available locally, except for a limited time with an AWS EC2 instance using our FourthBrain IAM accounts. We would like to deploy it on a public server so that it can be accessed by anyone. In the future, we would like to set up a public deployment using AWS Lambda to be as cost-efficient as possible. This would require some additional work to ensure that the app is secure and that the server is not overloaded by too many requests.
4. Currently, our deployment only supports classification of a single sequence at a time. In the future, we would like to add support for batch predictions, as well as the ability to upload a CSV or fasta file with sequences to classify.
5. Our application is missing some error checks with regards to the input sequence; it does not check for invalid characters and symbols. We would like to add these checks in the future.

## References
* [InstaDeep](https://www.instadeep.com/)
* [ProSE paper](https://www.cell.com/action/showPdf?pii=S2405-4712%2821%2900203-9)
* [ESM paper](https://www.biorxiv.org/content/10.1101/622803v4)

Bepler, T., Berger, B. Learning the protein language: evolution, structure, and function. Cell Systems 12, 6 (2021). https://doi.org/10.1016/j.cels.2021.05.017

Bepler, T., Berger, B. Learning protein sequence embeddings using information from structure. International Conference on Learning Representations (2019). https://openreview.net/pdf?id=SygLehCqtm

Rives, A., Meier, J., Sercu, T., Goyal, S., Lin, Z., Liu, J., Guo, D., Ott, M., Zitnick, C., Ma, J., & Fergus, R. (2019). Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250 Million Protein Sequences. bioRxiv. [https://www.biorxiv.org/content/10.1101/622803v1](https://www.biorxiv.org/content/10.1101/622803v1)

## Acknowledgements

We would like to thank InstaDeep for providing us with the data.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or issues running the deployment, please open an issue in this repo.
