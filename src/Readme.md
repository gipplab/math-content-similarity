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


### Obtaining train/test/validation split for training

We use zbRevCit as the main training data for our experiments. To obatin the train/test/validation split:

```
python traintestval.py 
```