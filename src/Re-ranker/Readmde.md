### Re-Ranker Candidates (Table 5)

To evaluate the performance of different re-rankers, follow these steps:

1. Run the following command to execute the re-ranker evaluation script:

   ```bash
   python custom_reranker.py
   ```

2. This script generates a result file for each re-ranker (e.g., `ltr_svm.csv`).

3. To compute evaluation scores, pass the generated file as an argument to the evaluation script:

   ```bash
   python src/getEvalScores.py /path/to/generated_recommendations.csv
   ```

---

### Performance Comparison of Re-Rankers on zbRevCit Dataset

The table below presents the performance metrics for various re-ranking models:

| Model                  | P@3   | P@5   | R@10  | MRR   | nDCG  |
|------------------------|-------|-------|-------|-------|-------|
| LTR-SVM               | 0.012 | 0.010 | 0.048 | 0.167 | 0.129 |
| LTR-LambdaMART        | 0.187 | 0.139 | 0.327 | 0.381 | 0.284 |
| Random Forest         | 0.081 | 0.047 | 0.201 | 0.197 | 0.156 |
| Logistic Regression   | 0.084 | 0.054 | 0.231 | 0.217 | 0.178 |
| **MathExRec Classifier** | **0.220** | **0.154** | **0.468** | **0.419** | **0.351** |

**Note:** The best-performing model in each category is highlighted in bold.