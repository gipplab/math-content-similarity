# Datasets

We introduce two datasets of Recommender System for research publications in Math created from zbMATH Open digital library.
zbRevCit: a large-scale dataset of over 350k recommendation pairs.
zbRevQuality: a high-quality small-scale dataset of 421 manually curated recommendations by an expert reviewer.

In the following, we explain how to obtain each dataset. 

# To view dataset's content online on zbMATH Open

## zbRevCit

We provide zbMATHOpen internal document identifier (docID) pairs in a csv file, with two columns:
document_id : docID for seed
recommendations: docIDs separated with ';' as recommendations for the seed

File with over 350K recommendation pairs: [zbRevCit.csv](https://drive.google.com/file/d/1Ps2I4jBMSURfHoFDrBEeBOtbVPR7Ei-I/view?usp=sharing)

To view content associated with each docID, please replace docID with the actual docID from the csv file in this URL: https://zbmath.org/docID

Example seed and recommendation pair for demonstration, please click on the link to view the document on the zbMATHOpen website:

| document_id | recommendations |
|-------------|-----------|
| [7061145](https://zbmath.org/7061145) | [1587695](https://zbmath.org/1587695) ;[1534319](https://zbmath.org/1534319) |
| [1102907](https://zbmath.org/1102907) | [3804385](https://zbmath.org/3804385) ;[3217604](https://zbmath.org/3217604) |


## zbRevQuality

Here we directly provide zbMATHOpen document identifier (docID) pairs in a csv file, with two columns:
- document_id : docID for seed
- recommendations: docIDs separated with ';' as recommendations for the seed

File with 421 recommendation pairs: [zbRevQuality.csv](https://drive.google.com/file/d/1Sr7fk1RSshNBAWNn6a_-Dsvbo1l4KD91/view?usp=sharing)

To view content associated with each docID, please replace docID with the actual docID from the csv file in this URL: https://zbmath.org/docID

Example seed and recommendation pair for demonstration, please click on the link to view the document on the zbMATHOpen website:

| document_id | recommendations |
|-------------|-----------|
| [1303018](https://zbmath.org/1303018) | [1587695](https://zbmath.org/1587695) ;[951967](https://zbmath.org/951967) ;[5354085](https://zbmath.org/5354085) ;[5120555](https://zbmath.org/5120555) ;[427914](https://zbmath.org/427914) ;[224045](https://zbmath.org/224045)|
| [1591097](https://zbmath.org/1591097) | [5049067](https://zbmath.org/5049067) ;[3867686](https://zbmath.org/3867686) ;[1758339](https://zbmath.org/1758339) ;[2136591](https://zbmath.org/2136591) |

ZbRevQuality is only used as test dataset.

# To view dataset's content offline

In order to view both the dataset's contents offline, we first use zbMATH Open [API](https://api.zbmath.org/v1/) to get contents of all documents of zbMATH Open in a casv file. This single file can then be used to obtain the contents of both datasets without again creating a separate file. 

To obtain all documents of zbMATH Open in a CSV file.

Run ```python zbMATHDocsData.py```   

Output: File zbMATHDocsData.csv created with fields
- document_id = zbMATHOPen unique document identifier
- text = review text 
- title = document title
- msc = mathematics subject classification codes for the document
- keyowrds = keywords for the document
- references = references for the document

## Sample data from zbMATHDocsData.csv

| document_id | text | title | msc | keywords | refrences |
|-------------|------|-------|------|------|------|
| [7973267](https://zbmath.org/7973267) | Summary: The Inverse Gaussian distribution finds application in various fields, such as finance, survival analysis, psychology, engineering, physics, and quality control . . .  | On the power of Gini index-based goodness-of-fit test for the inverse Gaussian distribution. |  {62G10: Nonparametric hypothesis testing, 62P30: Applications of statistics in engineering and industry; control charts} | (Gini index; type-I error; critical points; test power; Monte Carlo simulation) | (Alizadeh, H.N. (2017), Gini index-based goodness-of-fit test for the logistic distribution, Communications in Statistics-Theory and Methods, 46, 7114-7124., . . . . ) |

## Getting contents of zbRevCit & zbRevQuality

We have docIDs in both the downloaded files zbRevCit.csv and zbRevQuality.csv. 
In order to obtain contents of each docID please run the follwing script with parameter docID from dataset files.


```python offlinedata.py zb12345 --file my_data.csv```