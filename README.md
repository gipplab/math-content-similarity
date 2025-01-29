## About

This repository contains the resources of SIGIR'2025 submission "MATHRecSys: Recommender System for Math Research Papers"


### Install Dependencies

Please run the following to install dependencies for running the scripts to obtain results (it is recommended to create a virtual environment first and load it before you start loading data or running experiments).

```pip install -r requirements.txt```

### Dataset

Please refer to ```data``` folder of this repository to get information on how to download the data, obtain seed and recommendations pairs, and split (train/test/validation) used for traininng and tresting models of both zbRevCit and zbRev Quality datasets. 

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

To calculate evaluation scores (Precision, Recall, F1, MRR, nDCG), run

```reproducing_results/getEValscores.py```

Additionally, the evaluation results of the reranker stage on zbRevCit dataset are available in 

```reproducing_results/Re-ranker/evalresultsReranker.md```

## Organizers

[Anonymous]

## COntact

[ANonymous]