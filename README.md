## About

This repository contains the resources of SIGIR'2025 submission "MATHRecSys: Recommender System for Math Research Papers"

## Install Dependencies

If you want to have run any script in this repository (to load data, to obtain results, etc) please run the following to install dependencies. It is recommended to create a virtual environment first and then installing dependencies.

```pip install -r requirements.txt```

## Dataset

Please refer to ```data/Readme.md``` of this repository to get information on how dataset looks like, how to download it, obtain seed and recommendations pairs for both zbRevCit and zbRev Quality datasets.

## Demo

Please refer to the ```demo/Readme.md``` folder of this repository on how does the recommendations looks on the MarDI portal. 

## HyMathRec: Two-stage Recommender System

We proposed a two stage Recommender System that improves on baseline and on fine tuned Large Language Model.
We expect that you have a csv file with columns similar to ```zbMATHDocsData.csv```, explained in ```data/Readme.md```.
To generate ranked recommendations for a seed (docID:7952804), given n candidate recommendations, run the follwing script.

```python src/hyMathRec.py --file my_data.csv --docid  7952804```

This will generate ranked recommendations in a csv file, in decreaing order of likelihood. 

## Reproducing experiments

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

To get evaluation results of Re-ranker, go to follow the mentioned steps:

```src/Re-ranker/Readme.md```

## Contributers

[Anonymous]

## Contact

[ANonymous]