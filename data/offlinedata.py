import pandas as pd
import argparse

# Define function to load CSV and find document

def find_document(doc_id, file_path='zbMATHDocsData.csv'):
    try:
        # Load CSV file
        df = pd.read_csv(file_path)
        
        # Ensure the required columns exist
        required_columns = {'document_id', 'text', 'title', 'msc', 'keywords', 'references'}
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find document by docID')
    parser.add_argument('docID', type=str, help='Document ID to search')
    parser.add_argument('--file', type=str, default='zbMATHDocsData.csv', help='CSV file path')
    args = parser.parse_args()
    
    find_document(args.docID, args.file)
