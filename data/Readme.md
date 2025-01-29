# Dataset Obtaining and Utilization

Note: Please install depnedencies mentioned in ''

We introduce two Recommender System datasets created using research publications present at the zbMATHOpen library: 
zbRevCit: a large-scale dataset of over 350k recommendation pairs obtained by using reviewer's references in zbMATH Open.
zbRevQuality: a high-quality small-scaled dataset of 421 manually curated recommendations by an expert reviewer, yielding a greater set of expert-certified recommendations for each seed.

In the followinf, we first explain how to obtain all documents of zbMATHOPen library.

## Obtaining zbMATHOpen publications

zbMATHOpen provides API to access to all of its contents.

To get all documents run ```python zbMATHDocsData.py```
Output: File zbMATHDocsData.csv created with fields
document_id = zbMATHOPen unique document idenfier
text = review text 
title = document title
msc = mathematics subject classification codes for the document
keyowrds = keywords for the document
references = references for the document

### Sample data from zbMATHDocsData.csv

| document_id | text | title | msc | keywords | refrences |
|-------------|------|-------|------|------|------|
| [7973267](https://zbmath.org/7973267) | Summary: The Inverse Gaussian distribution finds application in various fields, such as finance, survival analysis, psychology, engineering, physics, and quality control . . .  | On the power of Gini index-based goodness-of-fit test for the inverse Gaussian distribution. |  {62G10: Nonparametric hypothesis testing, 62P30: Applications of statistics in engineering and industry; control charts} | (Gini index; type-I error; critical points; test power; Monte Carlo simulation) | (Alizadeh, H.N. (2017), Gini index-based goodness-of-fit test for the logistic distribution, Communications in Statistics-Theory and Methods, 46, 7114-7124., . . . . ) |     

## zbRevCit

The zbRevCit dataset consists of recommendations pairs obtained from reviews of zbMATHOpen. Within a review, reviewers may mention zbMATHOpen document IDs as in-review citations, which are considered as recommendations. 
Here we directly provide document ID pairs in a csv file, with two columns:
document_id : zbMATHOpen document identifier for seed
recommendations: zbMATHOpen document identifiers separated with ';' for recommendations

File with seed and recommendations pairs: [zbRevCit.csv](https://drive.google.com/file/d/1Ps2I4jBMSURfHoFDrBEeBOtbVPR7Ei-I/view?usp=sharing)

Example seed and recommendation pair for demonstration, please click on the link to view the document on the zbMATHOpen website:

| document_id | recommendations |
|-------------|-----------|
| [7061145](https://zbmath.org/7061145) | [1587695](https://zbmath.org/1587695) ;[1534319](https://zbmath.org/1534319) |
| [1102907](https://zbmath.org/1102907) | [3804385](https://zbmath.org/3804385) ;[3217604](https://zbmath.org/3217604) |

### Obtaining train/test/validation split for training

We use zbRevCit as the main training data for our experiments. To obatin the train/test/validation split:

```
python traintestval.py 
```

## zbRevQuality

The zbRevQuality dataset represents a single reviewer and their gold standard recommendations. 
Here we directly provide document ID pairs in a csv file, with two columns:
document_id : zbMATHOpen document identifier for seed
recommendations: zbMATHOpen document identifiers separated with ';' for recommendations

File with seed and recommendations pairs: https://drive.google.com/file/d/1Sr7fk1RSshNBAWNn6a_-Dsvbo1l4KD91/view?usp=sharing

Example seed and recommendation pair for demonstration, please click on the link to view the document on the zbMATHOpen website:

| document_id | recommendations |
|-------------|-----------|
| [1303018](https://zbmath.org/1303018) | [1587695](https://zbmath.org/1587695) ;[951967](https://zbmath.org/951967) ;[5354085](https://zbmath.org/5354085) ;[5120555](https://zbmath.org/5120555) ;[427914](https://zbmath.org/427914) ;[224045](https://zbmath.org/224045)|
| [1591097](https://zbmath.org/1591097) | [5049067](https://zbmath.org/5049067) ;[3867686](https://zbmath.org/3867686) ;[1758339](https://zbmath.org/1758339) ;[2136591](https://zbmath.org/2136591) |

ZbRevQuality is only used as test dataset.