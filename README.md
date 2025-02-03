## About

This repository contains the resources of SIGIR'2025 submission "MATHRecSys: Recommender System for Math Research Papers"

### Install Dependencies

If you want to have run any script in this repository (to load data, to obtain results, etc) please run the following to install dependencies. It is recommended to create a virtual environment first and then installing dependencies.

```pip install -r requirements.txt```

## Dataset

Please refer to ```data``` folder of this repository to get information on how dataset looks like, how to download it, obtain seed and recommendations pairs for both zbRevCit and zbRev Quality datasets.

## Demo

Please refer to the ```demo``` folder of this repository on how does the recommendations looks on the MarDI portal. 

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