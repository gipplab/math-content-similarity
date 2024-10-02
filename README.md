## About

This repository contains the resources used for ECIR'2025 submission "Learning from the Expert: Generating Recommendations Like an Expert Mathematician"


### Install Dependencies

Please run the following to install dependencies for running the scripts to obtain results (it is recommended to create a virtual environment first).

```pip install -r requirements.txt```

### Dataset

The documents are obtained via zbMATHOpen API https://api.zbmath.org/v1/
The ID of documents can be obtained from repo: https://zenodo.org/records/5062959

To obtain metadata if all documents such as title, abstract, keywords, MSCs, citations, author names, etc please run

```python /src/hybrid/feature_simil/getDataset.py```

## Evaluation results

### Baselin models (Table 2)

To get evaluation results of basline, please go to follow the mentioned steps:

```reproducing_results/Baseline/```

### Initial Ranker candidates (Table 3)

To get evaluation results of Initial Ranker, go to follow the mentioned steps:

```reproducing_results/InitialRanker/```

### Re-anker candidates (Table 4)

To get evaluation results of Re-ranker, go to follow the mentioned steps:

```reproducing_results/Re-ranker/```