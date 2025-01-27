![Re-ranker results on zbRevCit](./)

### Performance Comparison of Re-rankers on zbRevCit Dataset

| Model                     | P@3   | P@5   | R@10  | MRR   | nDCG  |
|---------------------------|-------|-------|-------|-------|-------|
| LTR-SVM                  | 0.012 | 0.010 | 0.014 | 0.022 | 0.005 |
| LTR-lambdaMART           | 0.199 | 0.231 | 0.184 | 0.325 | 0.195 |
| Randomforest             | 0.107 | 0.108 | 0.079 | 0.138 | 0.187 |
| Logit                    | 0.098 | 0.067 | 0.123 | 0.188 | 0.096 |
| MathExRec_Classifier     | **0.333** | **0.282** | **0.390** | **0.481** | **0.251** |
