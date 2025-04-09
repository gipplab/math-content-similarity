## About

This repository contains the resources of RecSys'2025 submission "MATHRecSys: Recommender System for Math Research Papers"

## Install Dependencies

If you want to have run any script in this repository (to load data, to obtain results, etc) please run the following to install dependencies. It is recommended to create a virtual environment first and then installing dependencies.

```pip install -r requirements.txt```

## Dataset

Please refer to [data/Readme.md](data/Readme.md) of this repository to get information on how used datasets looks like, how to download it, obtain seed and recommendations pairs for both zbRevCit and zbRevQuality datasets.

## Demo

Please refer to the [demo/Readme.md](demo/Readme.md) folder of this repository on how does the recommendations looks on the MarDI portal. 

## Additional Result Table

The results of the re-ranker on zbRevCit is available in [src/Re-ranker/Readmde.md](src/Re-ranker/Readmde.md).

## Reproducing Results

We expect that you have a csv file with columns similar to ```zbMATHDocsData.csv``` (explained in [data/Readme.md](data/Readme.md)).
To generate top 10 ranked recommendations for a document (e.g., docID: 7952804), please go to the following page and follow mentioned intructions in: [src/HyMathRec/Readmde.md](src/HyMathRec/Readmde.md)

### Baseline models (Table 2)

To get evaluation results of baseline, please follow the mentioned steps:

```src/base_models/Readme.md```


### Fine tuned Stella (Table 3)

To get evaluation results of fine tuned stella, please follow the mentioned steps:

```src/stella_finetune/Readme.md```

### Initial Ranker candidates (Table 4)

To get evaluation results of Initial Ranker, please follow the mentioned steps:

```src/InitialRanker/Readme.md```

### Re-anker candidates (Table 5)

To get evaluation results of Re-ranker and the evaluation results of the reranker on zbRevCit dataset please refer to:

```src/Re-ranker/Readme.md```

## Contributers

[Anonymous]

## Contact

[ANonymous]
