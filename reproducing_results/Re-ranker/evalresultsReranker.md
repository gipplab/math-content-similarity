### Performance Comparison of Re-rankers on zbRevCit Dataset

| Model                     | P@3   | P@5   | R@10  | MRR   | nDCG  |
|---------------------------|-------|-------|-------|-------|-------|
| LTR-SVM                  | 0.012 | 0.010 | 0.048 | 0.167 | 0.129 |
| LTR-lambdaMART           | 0.187 | 0.139 | 0.327 | 0.381 | 0.284 |
| Randomforest             | 0.081 | 0.047 | 0.201 | 0.197 | 0.156 |
| Logit                    | 0.084 | 0.054 | 0.231 | 0.217 | 0.178 |
| MathExRec_Classifier     | **0.220** | **0.154** | **0.468** | **0.419** | **0.351** |
