# Datasets

We introduce two datasets of Recommender System for research publications in Math created from zbMATH Open digital library.
zbRevCit: a large-scale dataset of over 350k recommendation pairs.
zbRevQuality: a high-quality small-scale dataset of 421 manually curated recommendations by an expert reviewer.

In the following, we explain how does each dataset looks like and how to obtain its contents.

## zbRevCit

Here we directly provide zbMATHOpen document identifier (docID) pairs in a csv file, with two columns:
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
document_id : docID for seed
recommendations: docIDs separated with ';' as recommendations for the seed

File with 421 recommendation pairs: [zbRevQuality.csv](https://drive.google.com/file/d/1Sr7fk1RSshNBAWNn6a_-Dsvbo1l4KD91/view?usp=sharing)

To view content associated with each docID, please replace docID with the actual docID from the csv file in this URL: https://zbmath.org/docID

Example seed and recommendation pair for demonstration, please click on the link to view the document on the zbMATHOpen website:

| document_id | recommendations |
|-------------|-----------|
| [1303018](https://zbmath.org/1303018) | [1587695](https://zbmath.org/1587695) ;[951967](https://zbmath.org/951967) ;[5354085](https://zbmath.org/5354085) ;[5120555](https://zbmath.org/5120555) ;[427914](https://zbmath.org/427914) ;[224045](https://zbmath.org/224045)|
| [1591097](https://zbmath.org/1591097) | [5049067](https://zbmath.org/5049067) ;[3867686](https://zbmath.org/3867686) ;[1758339](https://zbmath.org/1758339) ;[2136591](https://zbmath.org/2136591) |

ZbRevQuality is only used as test dataset.