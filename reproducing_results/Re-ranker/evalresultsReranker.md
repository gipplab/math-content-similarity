![Re-ranker results on zbRevCit](./)

### Performance Comparison of Re-rankers on zbRevCit Dataset

| Model                     | P@3   | P@5   | R@10  | MRR   | nDCG  |
|---------------------------|-------|-------|-------|-------|-------|
| LTR-SVM                  | 0.012 | 0.010 | 0.014 | 0.022 | 0.005 |
| LTR-lambdaMART           | 0.199 | 0.151 | 0.206 | 0.337 | 0.160 |
| Randomforest             | 0.097 | 0.091 | 0.111 | 0.221 | 0.084 |
| Logit                    | 0.098 | 0.067 | 0.123 | 0.188 | 0.096 |
| MathExRec_Classifier     | **0.333** | **0.282** | **0.390** | **0.481** | **0.251** |
