# Datasets

## Overview
This repository provides two datasets for recommender system for mathematical publications. They are derived from the zbMATH Open digital library.

- **zbRevCit**: A large-scale dataset with over **350,000 recommendation pairs**.
- **zbRevQuality**: A **high-quality, manually curated** dataset containing **421 expert-reviewed recommendations**.

Below, we explain how to obtain and use each dataset.

---

## Viewing Dataset Contents Online on zbMATH Open website

## zbRevCit

We provide zbMATHOpen document identifier (docID) pairs in a CSV file, with two columns:

| Column | Description |
|--------|-------------|
| `document_id` | docID of the seed document |
| `recommendations` | docIDs of recommended documents, separated by `;` |

🔗 **Download** zbRevCit dataset file with over 350K recommendation pairs: [zbRevCit.csv](https://drive.google.com/file/d/1Ps2I4jBMSURfHoFDrBEeBOtbVPR7Ei-I/view?usp=sharing).

To view the document associated with a docID, replace `docID` in the following URL with an actual document ID:
```
https://zbmath.org/docID
```

🔹 **Example:** seed and recommendation pair for demonstration with hyperlinked URLs, please click on the link to view the document on the zbMATH Open website:

| document_id | recommendations |
|-------------|-----------|
| [7061145](https://zbmath.org/7061145) | [1587695](https://zbmath.org/1587695) ; [1534319](https://zbmath.org/1534319) |
| [1102907](https://zbmath.org/1102907) | [3804385](https://zbmath.org/3804385) ; [3217604](https://zbmath.org/3217604) |



## **zbRevQuality**

**Description:** This dataset follows the same structure as zbRevCit but contains expert-reviewed recommendations.

🔗 **Download** zbRevQuality dataset file with 120 recommendation pairs: [zbRevQuality.csv](https://drive.google.com/file/d/1Sr7fk1RSshNBAWNn6a_-Dsvbo1l4KD91/view?usp=sharing)

🔹 **Example:**
| document_id | recommendations |
|-------------|-----------|
| [1303018](https://zbmath.org/1303018) | [1587695](https://zbmath.org/1587695) ; [951967](https://zbmath.org/951967) ; [5354085](https://zbmath.org/5354085) ; [5120555](https://zbmath.org/5120555) ; [427914](https://zbmath.org/427914) ; [224045](https://zbmath.org/224045) |
| [1591097](https://zbmath.org/1591097) | [5049067](https://zbmath.org/5049067) ; [3867686](https://zbmath.org/3867686) ; [1758339](https://zbmath.org/1758339) ; [2136591](https://zbmath.org/2136591) |

📌 **Note:** ZbRevQuality is only used as test dataset.

---


# Viewing Dataset Contents Offline

In order to view both the dataset's contents offline, we first use zbMATH Open [API](https://api.zbmath.org/v1/) to get contents of all documents of zbMATH Open in a CSV file. This single file can then be used to obtain the contents of both datasets without again fetching the data from API. 

### **Step 1: Download zbMATH Open Documents**

To obtain all documents of zbMATH Open in a CSV file.

Run ```python zbMATHDocsData.py```   

📄 **produces a csv File:** `zbMATHDocsData.csv` containing:

| Column | Description |
|--------|-------------|
| `document_id` | Unique zbMATH Open document identifier |
| `text` | Review text |
| `title` | Document title |
| `msc` | Mathematics Subject Classification (MSC) codes |
| `keywords` | Keywords associated with the document |
| `references` | References cited in the document |


**Sample data from zbMATHDocsData.csv:**

| document_id | text | title | msc | keywords | refrences |
|-------------|------|-------|------|------|------|
| [7973267](https://zbmath.org/7973267) | Summary: The Inverse Gaussian distribution finds application in various fields, such as finance, survival analysis, psychology, engineering, physics, and quality control . . .  | On the power of Gini index-based goodness-of-fit test for the inverse Gaussian distribution. |  {62G10: Nonparametric hypothesis testing, 62P30: Applications of statistics in engineering and industry; control charts} | (Gini index; type-I error; critical points; test power; Monte Carlo simulation) | (Alizadeh, H.N. (2017), Gini index-based goodness-of-fit test for the logistic distribution, Communications in Statistics-Theory and Methods, 46, 7114-7124., . . . . ) |

### **Step 2: Extract Content for zbRevCit & zbRevQuality**

Once `zbMATHDocsData.csv` is available, use it to extract documents associated with docIDs in the recommendation datasets.

**Run the following command:**
```sh
python offlinedata.py docID --file zbMATHDocsData.csv
```

📌 **This script fetches document details based on docID from the downloaded dataset.**