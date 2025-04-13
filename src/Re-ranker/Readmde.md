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