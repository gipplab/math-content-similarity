import os
import sys
import pickle
import torch
import numpy as np
import pandas as pd
import argparse
from torch.nn.functional import cosine_similarity
from transformers import LongformerModel, LongformerTokenizer

def load_features():
    """ Load all features"""
    dir_feat = "SeqRecExp/zbDataReRanker/dataFeatures/"
    features_ = {
        "feat_abs": pickle.load(open(dir_feat + "initRank_featAbstr.pkl", "rb")),
        "feat_kwrd": pickle.load(open(dir_feat + "initRank_featKwrd.pkl", "rb")),
        "feat_ref": pickle.load(open(dir_feat + "initRank_featRefrnc.pkl", "rb")),
        "feat_mscs": pickle.load(open(dir_feat + "initRank_featMSCs.pkl", "rb")),
        "feat_title": pickle.load(open(dir_feat + "initRank_featTitle.pkl", "rb"))
    }
    return features_

def getdocString(doc_id, features):
    """Given ID and features, return a concatenated feature string"""
    oneHotstr = ""
    for key in features.keys():
        feature_dict = features[key]
        if doc_id in feature_dict:
            oneHotstr += feature_dict[doc_id] + " "
    return oneHotstr.strip()

def get_longformer_model():
    """Load the Longformer model and tokenizer"""
    model_name = 'myFNN'
    tokenizer = LongformerTokenizer.from_pretrained(model_name)
    model = LongformerModel.from_pretrained(model_name)
    model.eval()
    return model, tokenizer

def get_longformer_embeddings(documents, model, tokenizer, batch_size=100):
    """Generate embeddings for a list of documents using Longformer."""
    all_embeddings = []
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        encoded = tokenizer(batch_docs, add_special_tokens=True, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**encoded)
            batch_embeddings = outputs.last_hidden_state[:, 0, :]
        all_embeddings.append(batch_embeddings)
    return torch.cat(all_embeddings, dim=0)

def rank_recommendations(seed_document, recommendations, model, tokenizer):
    """Rank recommendations based on cosine similarity to the seed document."""
    documents = [seed_document] + recommendations
    embeddings = get_longformer_embeddings(documents, model, tokenizer)
    seed_emb = embeddings[0].unsqueeze(0)
    rec_embs = embeddings[1:]
    similarities = cosine_similarity(seed_emb, rec_embs).squeeze()
    scored_recommendations = sorted(zip(recommendations, similarities.tolist()), key=lambda x: x[1], reverse=True)
    return scored_recommendations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--docid", type=str, required=True, help="Document ID for recommendation ranking")
    args = parser.parse_args()
    
    # Load features and model
    features = load_features()
    model, tokenizer = get_longformer_model()
    
    # Load dataset
    df = pd.read_csv(args.file)
    if args.docid not in df['doc_id'].astype(str).values:
        print("Document ID not found in dataset.")
        sys.exit(1)
    
    # Extract document and recommendations
    seed_str = getdocString(args.docid, features)
    recommendations = [getdocString(str(doc), features) for doc in df['doc_id'].astype(str).values if str(doc) != args.docid]
    
    # Rank recommendations
    ranked_recs = rank_recommendations(seed_str, recommendations, model, tokenizer)
    
    # Save to CSV
    output_df = pd.DataFrame(ranked_recs, columns=["doc_id", "likelihood"])
    output_file = f"ranked_recommendations_{args.docid}.csv"
    output_df.to_csv(output_file, index=False)
    print(f"Ranked recommendations saved to {output_file}")
    
if __name__ == "__main__":
    main()