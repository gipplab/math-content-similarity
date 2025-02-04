import argparse
import numpy as np

def mean_reciprocal_rank(ideal_recommendations, generated_recommendations):
    """ Mean Reciprocal Rank (MRR) measures how soon the first relevant result is returned."""
    mrr = 0
    for ideal, generated in zip(ideal_recommendations, generated_recommendations):
        for i, rec in enumerate(generated):
            if rec in ideal:
                mrr += 1 / (i + 1)
                break
    return mrr / len(ideal_recommendations)

def dcg_at_k(recommendations, ideal, k):
    """Calculate the Discounted Cumulative Gain at k."""
    dcg = 0.0
    for i in range(min(k, len(recommendations))):
        if recommendations[i] in ideal:
            dcg += 1 / np.log2(i + 2)  # using i+2 to start at log2(2) = 1
    return dcg

def ndcg_at_k(ideal_recommendations, generated_recommendations, k):
    """
    Normalized Discounted Cumulative Gain (nDCG) measures the quality of the recommendations
    by comparing the recommended order with the ideal order.
    """
    ndcg_total = 0
    for ideal, generated in zip(ideal_recommendations, generated_recommendations):
        ideal_dcg = dcg_at_k(ideal, ideal, k)  # DCG for ideal list
        actual_dcg = dcg_at_k(generated, ideal, k)  # DCG for the generated list
        ndcg = actual_dcg / ideal_dcg if ideal_dcg > 0 else 0
        ndcg_total += ndcg
    return ndcg_total / len(ideal_recommendations)

def precision_at_k(ideal_recommendations, generated_recommendations, k):
    """P@k measures how many of the top k recommendations are relevant."""
    precision_total = 0
    for ideal, generated in zip(ideal_recommendations, generated_recommendations):
        relevant = len([rec for rec in generated[:k] if rec in ideal])
        precision_total += relevant / k
    return precision_total / len(ideal_recommendations)

def recall_at_k(ideal_recommendations, generated_recommendations, k=10):
    """R@k measures how many of the relevant items are found in the top k recommendations."""
    recall_total = 0
    for ideal, generated in zip(ideal_recommendations, generated_recommendations):
        relevant = len([rec for rec in generated[:k] if rec in ideal])
        recall_total += relevant / len(ideal)
    return recall_total / len(ideal_recommendations)

# Sample input
#ideal_recommendations = [['rec1', 'rec2'], ['rec3', 'rec4']]
#generated_recommendations = [['rec5', 'rec6'], ['rec7', 'rec8']]
def main(ideal_recommendations, generated_recommendations):
    # Calculate MRR, nDCG@5, P@3, P@5, and Recall
    mrr = mean_reciprocal_rank(ideal_recommendations, generated_recommendations)
    ndcg_5 = ndcg_at_k(ideal_recommendations, generated_recommendations, 5)
    precision_3 = precision_at_k(ideal_recommendations, generated_recommendations, 3)
    precision_5 = precision_at_k(ideal_recommendations, generated_recommendations, 5)
    recall_ = recall_at_k(ideal_recommendations, generated_recommendations)
    recall_1k = recall_at_k(ideal_recommendations, generated_recommendations, 4000)
    return precision_3, precision_5, recall_, recall_1k, mrr, ndcg_5

def read_results_file(file_path,split='test'):
    if split=='test':
        split_df = test_
    elif split=='train':
        split_df = train_
    else:
        split_df = valid_
    getallfls = os.listdir(file_path)
    genRecmnds, idealRecmnds = [], []
    for i,eachF in enumerate(getallfls):
        with open(file_path+eachF, 'r') as json_file:
            # Load the content of the file into a Python dictionary
            data = json.load(json_file)
            try:
                list_true = isinstance(data[list(data.keys())[0]][0],list)
            except:
                list_true = isinstance(data[list(data.keys())[1]][0],list)
        for eackDoc in data.keys():
            if eackDoc in intersection: # check if we have data for this seed
                idl_recmnds = idlRecommendations(eackDoc,split_df)
                if set(idl_recmnds).issubset(intersection_cit): #check if we have data for both recmnds
                    if len(idl_recmnds) == 0:
                        print(eackDoc)
                    idealRecmnds.append(idl_recmnds)
                    if list_true:
                        gen_recmnds = [str(ea_[0]) for ea_ in data[eackDoc][:10]]
                    else:
                        gen_recmnds = [str(ea_) for ea_ in data[eackDoc][:10]]
                    genRecmnds.append(gen_recmnds)
    p3, p5, r_, mrr_, ndcg_ = eval_metrics.main(idealRecmnds, genRecmnds)

    print(p3, p5, r_, mrr_, ndcg_)

def read_results_file(file_path, split='test'):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        results = [line.strip() for line in lines if split in line]
        return results
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a results file and filter by split.")
    parser.add_argument("file_path", type=str, help="Path to the results file")
    parser.add_argument("--split", type=str, default="test", help="Split type to filter (default: 'test')")

    args = parser.parse_args()

    results = read_results_file(args.file_path, args.split)
    if results:
        for line in results:
            print(line)
