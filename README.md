## About

This repository contains the resources used for SIGIR'2025 submission "MATHRecSys: Recommender System for Math Research Papers"


### Install Dependencies

Please run the following to install dependencies for running the scripts to obtain results (it is recommended to create a virtual environment first).

```pip install -r requirements.txt```

### Dataset

Please refer to ```data_``` folder of the repository

## Evaluation results

### Baselin models (Table 2)

To get evaluation results of basline, please go to follow the mentioned steps:

```reproducing_results/Baseline/```


### Fine tuned Stella (Table 3)

To get evaluation results of fine tuned stella, please go to follow the mentioned steps:

```reproducing_results/Baseline/```

### Initial Ranker candidates (Table 4)

To get evaluation results of Initial Ranker, go to follow the mentioned steps:

```reproducing_results/InitialRanker/```

### Re-anker candidates (Table 5)

To get evaluation results of Re-ranker, go to follow the mentioned steps:

```reproducing_results/Re-ranker/```

To calculate Kappa scores and evaluation scores (Precision, Recall, F1, MRR, nDCG), run

```python src/hybrid/userAnnoEval.py```


Additionally, the evaluation results of the reranker stage are available in 

```python reproducing_results/Re-ranker/Readmde.md```