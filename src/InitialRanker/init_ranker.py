import faiss
import pickle
import argparse
import pandas as pd
from collections import defaultdict
from sentence_transformers import SentenceTransformer

INSTRUCTIONS = {
    "qa": {
        "query": "Instruct: Retrieve semantically similar text.\nQuery: ",
        "key": "",
    },
}

def getComplData(file_path):
    """returns dataframe of whole zbMATHOpen"""
    df = pd.read_csv(file_path)      
    # Ensure the required columns exist
    required_columns = {'document_id', 'text', 'title', 'msc', 'keywords', 'references', 'references_id'}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV file is missing required columns")
    return df

def getdoccont(doc_id, feat_, main_data):
    try:
        df = main_data
        # Find row where document_id matches the given docID
        row = df[df['document_id'] == doc_id]
        if row.empty:
            print(f"No document found with ID: {doc_id}")
        else:
            # Check if feat_ is a valid column in the dataframe
            if feat_ in row.columns:
                return row[feat_].iloc[0]  # Return the value of the requested feature
            else:
                print(f"Feature '{feat_}' not found in the document.")
    except Exception as e:
        print(f"Error: {e}")

def getRefStrings(df_maindata, doc_id):
    try:
        X = None  # The matched string
        Y = None  # The list of references for the matching doc_id
        # Find the row where 'document_id' matches the given doc_id
        row = df_maindata[df_maindata['document_id'] == doc_id]
        if row.empty:
            print(f"No document found with ID: {doc_id}")
            return None, None
        # Extract the references list for the given doc_id
        Y = row['references'].iloc[0]
        # Now find the reference_id in the dataframe that matches any of the reference ids
        for index, reference_id_list in enumerate(df_maindata['references_id']):
            # Check if the reference_id list contains the document_id
            if doc_id in reference_id_list:
                X = reference_id_list
                reference_for_match = [df_maindata['references'].iloc[index]]
                # If a match is found, return the string X (matched references_id) and the list Y (references for the doc_id)
                return X, reference_for_match
        print(f"No matching reference_id found for doc_id {doc_id}")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def getRefRanked(doc_id_, main_data, model_dir):
    ref_strings, seed_str = getRefStrings(main_data, doc_id_)
    instruction = INSTRUCTIONS["qa"]
    model = SentenceTransformer(model_dir, device='cuda', trust_remote_code=True)
    embedding_dim = model.get_sentence_embedding_dimension()
    seedEmbed = model.encode(seed_str, convert_to_numpy=True, device='cuda')
    potrefEmbed = model.encode(ref_strings, convert_to_numpy=True, device='cuda')
    similarities = faiss.index_CPU().cosine_similarity(seedEmbed, potrefEmbed)
    combined_ = list(zip(ref_strings, similarities[0]))
    sorted_combined_ = sorted(combined_, key=lambda x: x[1], reverse=True)
    return sorted_combined_

def createIndex(main_data_,used_data,model_name_or_path):
    print("Create index for: ",used_data)
    instruction = INSTRUCTIONS["qa"]
    model = SentenceTransformer(model_name_or_path, device='cuda', trust_remote_code=True)
    embedding_dim = model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatIP(embedding_dim)
    batch_size = 5000
    for start_idx in range(0, len(main_data_), batch_size):
        print(start_idx,flush=True)
        end_idx = min(start_idx + batch_size, len(main_data_))
        titles_batch = main_data_[used_data].iloc[start_idx:end_idx].tolist()
        embeddings_batch = model.encode(titles_batch, convert_to_numpy=True, device='cuda')
        faiss.normalize_L2(embeddings_batch)
        index.add(embeddings_batch.astype('float32'))
    faiss.write_index(index, f"feat_/{used_data}_.index")

def creatIndexes(main_data_, model_dir):
    """Creating FAISS index for each feature"""
    createIndex(main_data_,'text',model_name_or_path=model_dir) # feat abstract
    createIndex(main_data_,'title',model_name_or_path=model_dir) # feat title
    createIndex(main_data_,'msc',model_name_or_path=model_dir) # feat msc
    createIndex(main_data_,'keywords',model_name_or_path=model_dir) # feat keywords
    # for keywords we don't need index, direct initial ranked list can be generated 

def getInitRankedDoc(doc_id_, model_dir, main_data):
    instruction = INSTRUCTIONS["qa"]
    model = SentenceTransformer(model_dir, device='cuda', trust_remote_code=True)
    num_scores = 1000 #number of ranked docs
    embedding_dim = model.get_sentence_embedding_dimension()
    results_ = {}
    for feat_ in ['text', 'title', 'msc', 'keywords']:
        index = faiss.read_index(f"feat_/{feat_}_.index")
        doc_content = getdoccont(doc_id_, feat_, main_data)
        embeddings_batch = model.encode([doc_content], convert_to_numpy=True, device='cuda')
        faiss.normalize_L2(embeddings_batch)
        scores, ranked_indices = index.search(embeddings_batch, num_scores)
        ranked_doc_ids = [(main_data['document_id'].iloc[idx_],score) for score,idx_ in zip(scores[0],ranked_indices[0])]
        results_[feat_] = ranked_doc_ids
    results_['references'] = getRefRanked(doc_id_, main_data, model_dir)
    with open('initRanked.pkl', 'wb') as file:  # this file will be used by ReRanker
        pickle.dump(final_list, file)
    combined_list = []
    for key in results_.keys():
        combined_list.extend(results_[key])
    combined_list.sort(key=lambda x: x[1], reverse=True)
    doc_id_dict = defaultdict(int)
    final_list = []
    for doc_id, score in combined_list:
        if doc_id not in doc_id_dict or score > doc_id_dict[doc_id]:
            doc_id_dict[doc_id] = score
            final_list.append((doc_id, score))
        if len(final_list) == 1000:
            break
    with open('initRanked_results.pkl', 'wb') as file: # These are the final ranked results for InitialRanker
        pickle.dump(final_list, file)

def main():
    parser = argparse.ArgumentParser(description="Rank documents based on HyMathRec initial ranker.")
    parser.add_argument('--docID', type=str, required=True, help="Document ID to rank")
    args = parser.parse_args()
    zbdata_dir = '../data/zbMATHDocsData.csv' # generated with zbMATHDocsData.py
    main_data_ = getComplData(zbdata_dir)    
    model_dir = "dunzhang/stella_en_400M_v5"
    doc_id = args.docID 
    creatIndexes(main_data_, model_dir)
    getInitRankedDoc(doc_id, model_dir, main_data_)

if __name__ == "__main__":
    main()