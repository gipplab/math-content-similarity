## Evaluation results

### Baselin models (Table 2)

- Base models

- Stella/Stella-ref/bge-en/llm-embedder/DPR/QWEN

```python /src/base_models/abstract_simil.py```

- QWEN

For recreating the LLM2Vec model, we applied the MNTP and SIMCSE procedures of LLM2Vec https://github.com/McGill-NLP/llm2vec to https://huggingface.co/Qwen/Qwen2.5-Math-1.5B.

- Approach0

We utlize Pya0 https://github.com/approach0/pya0 for indexing all formulae from zbMATHOpen

Then run

```python /src/base_models/mabowdor.py```

- Feature Refereces

```python /src/base_models/co_citation.py```
