import pandas as pd
import argparse
import math

def find_document(doc_id, file_path='zbMATHDocsData.csv'):
    #to load CSV and find document
    try:
        # Load CSV file
        df = pd.read_csv(file_path)      
        # Ensure the required columns exist
        required_columns = {'document_id', 'text', 'title', 'msc', 'keywords', 'references', 'references_id'}
        if not required_columns.issubset(df.columns):
            raise ValueError("CSV file is missing required columns")
        # Find row where document_id matches the given docID
        row = df[df['document_id'] == doc_id]
        if row.empty:
            print(f"No document found with ID: {doc_id}")
        else:
            print(row.to_dict(orient='records')[0])
    except Exception as e:
        print(f"Error: {e}")

def split_list(doc_ids, train_ratio, test_ratio, val_ratio):
    total_count = len(doc_ids)
    # Compute split sizes
    train_size = math.floor(total_count * train_ratio)
    test_size = math.floor(total_count * test_ratio)
    val_size = math.floor(total_count * val_ratio)
    # If the sizes don't perfectly sum up to total_count, add remaining samples to train
    remainder = total_count - (train_size + test_size + val_size)
    train_size += remainder  # Add remaining samples to train
    train_split = doc_ids[:train_size]
    test_split = doc_ids[train_size:train_size + test_size]
    val_split = doc_ids[train_size + test_size:]
    return train_split, test_split, val_split

def split_dataframe(df, train_ratio=0.6, test_ratio=0.2, val_ratio=0.2):
    citation_length_dict = {}
    # Populate the dictionary
    for index, row in df.iterrows():
        doc_id = row['document_id']
        citations = row['citation_de'].split(';')
        length = len(citations)
        if length not in citation_length_dict:
            citation_length_dict[length] = []
        citation_length_dict[length].append(doc_id)
    train_ids, test_ids, validation_ids = [], [], []
    for length, doc_ids in citation_length_dict.items():
        train_split, test_split, val_split = split_list(doc_ids, train_ratio, test_ratio, val_ratio)
        train_ids.extend(train_split)
        test_ids.extend(test_split)
        validation_ids.extend(val_split)
    # Filter the original dataframe to create the final train, test, validation sets
    if 'citations_list' in df.keys():
        keys_list = ['document_id','citation_de','citations_list']
    else:
        keys_list = ['document_id','citation_de']
    train_ = df[df['document_id'].isin(train_ids)][keys_list]
    test_ = df[df['document_id'].isin(test_ids)][keys_list]
    validation_ = df[df['document_id'].isin(validation_ids)][keys_list]
    return train_, test_, validation_


def getdata():
    data_ = "data/citation_dataset.csv"
    df = pd.read_csv(data_)
    df = df[df['reviewer'] != 0]
    train, test, val = split_dataframe(df)
    return train, test, val

def LoadDataFromFile():
    data_ = "data/citation_dataset.csv"
    df = pd.read_csv(data_)
    df = df[df['reviewer'] != 0]
    train, test, val = split_dataframe(df)
    print("column in train, test and valid looks like: ", train.columns.tolist(), test.columns.tolist(), val.columns.tolist())
    print("size of train, test and vali: ", train.shape[0], test.shape[0], val.shape[0])
    print("if it has any weird things: ", train.isna().sum().sum(), test.isna().sum().sum(), val.isna().sum().sum())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find document by docID')
    parser.add_argument('docID', type=str, help='Document ID to search')
    parser.add_argument('--file', type=str, default='zbMATHDocsData.csv', help='CSV file path')
    args = parser.parse_args()
    
    find_document(args.docID, args.file)