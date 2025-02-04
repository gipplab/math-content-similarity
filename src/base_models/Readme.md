## Evaluation results

### Baselin models (Table 2)

- Base models

- Stella/Stella-ref/bge-en/llm-embedder/DPR

```python abstract_simil.py```

Please replace model_dir with the base model path.

Stella & Stella-ref = NovaSearch/stella_en_400M_v5
bge-en = BAAI/bge-base-en-v1.5
llm-embedder = BAAI/llm-embedder
DPR = approach0/dpr-cocomae-320

- QWEN

For recreating the LLM2Vec model, we applied the MNTP and SIMCSE procedures of LLM2Vec https://github.com/McGill-NLP/llm2vec to https://huggingface.co/Qwen/Qwen2.5-Math-1.5B.

- Approach0

We utlize Pya0 https://github.com/approach0/pya0 for indexing all formulae from zbMATHOpen

Then run

```python /src/base_models/mabowdor.py```

- Feature Refereces

```python /src/base_models/co_citation.py```

## To calculate evaluation scores (Precision, Recall, F1, MRR, nDCG), run

```python src/getEValscores.py /path/to/generatedrecommendations.csv```