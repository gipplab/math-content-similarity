import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from src import getEValscores
from src.InitialRanker import init_ranker
from data import offlinedata


def getInitialRankData():
    train, test, val = offlinedata.getdata()
    #print("column in train, test and valid looks like: ", train.columns.tolist(), test.columns.tolist(), val.columns.tolist())
    #print("size of train, test and vali: ", train.shape[0], test.shape[0], val.shape[0])
    #print("if it has any empty cells: ", train.isna().sum().sum(), test.isna().sum().sum(), val.isna().sum().sum())
    init_ranker.saveInitiCandsnew(test)
    for index, row in val.iterrows():
        doc_id = int(row['document_id'])
        getInitiaLRankedcands = init_ranker.geTInitialRankedCands(doc_id)
        print(getInitiaLRankedcands)
        break

def idlRecommendations(doc_id,split):
    try:
        doc_here = split[split['document_id'] == int(doc_id)]['citation_de'].values[0]
        return doc_here.split("; ")
    except:
        print(split[split['document_id'] == int(doc_id)]['citation_de'].values)
        print("No ideal recmnds: ", doc_id, flush=True)
        return ["111111"]

def getLabelledData(_pickle, df_here):
    alldirs = os.listdir(_pickle)
    feature_ids = {
        'text': 1,
        'title': 2,
        'msc': 3,
        'keywords': 4,
        'references': 5
    }
    dictData = {}
    count_label, poslb = 0, 0
    for each_p in alldirs:
        with open(_pickle+each_p, "rb") as f:
            data_dict = pickle.load(f)
        for eachKe in data_dict.keys():
            listInData = []
            idlRecmnds = [str(idlr) for idlr in idlRecommendations(eachKe, df_here)]
            for eachFeat in data_dict[eachKe].keys():
                pos_s, neg_s = [], []
                for ele_ in data_dict[eachKe][eachFeat][1:]:
                    if str(ele_[0]) in idlRecmnds:
                        pos_s.append((ele_[0], ele_[1], feature_ids[eachFeat], 1.0))
                        poslb += 1
                    else:
                        neg_s.append((ele_[0], ele_[1], feature_ids[eachFeat], 0.0))
                listInData += pos_s
                count_label += len(neg_s[0:len(pos_s)])
                listInData += neg_s[0:len(pos_s)]
            dictData[eachKe] = listInData
    print("positive labels: ", count_label, poslb)
    print(len(dictData))
    #sys.exit(0)
    return dictData

def getHyMathRec_classifierResults():
    train, test, val = offlinedata.getdata()
    data_dict = getLabelledData("data/results/initRanker/validation_s/", val)
    test_dict = getLabelledData("data/results/initRanker/test_s/", test)
    print("len of train and test", len(train_data), len(test_data))
    # Prepare training data (score, feat_id) with label
    train_X = []  # Features (score, feat_id)
    train_y = []  # Labels
    for key, value in train_data:
        for doc_id, score, feat_id, label in value:
            train_X.append([score, feat_id])
            train_y.append(label)
    train_X = np.array(train_X)
    train_y = np.array(train_y)
    #print("len of train y and x", len(train_y), len(train_X))
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(train_X)
    # Initialize and train the MLPClassifier
    nn_clf = MLPClassifier(hidden_layer_sizes=(15, 15), max_iter=1000, random_state=42)
    nn_clf.fit(X_scaled, train_y)
    # Prepare test data (score, feat_id) and predict labels with probabilities
    test_results = {}
        for key, value in test_data:
        test_X = []
        for doc_id, score, feat_id, label in value:
            test_X.append([score, feat_id])
        if len(test_X) != 0:
            test_X = np.array(test_X)
            test_X_scaled = scaler.transform(test_X)
            # Predict the probabilities and labels for the test data
            test_probs = nn_clf.predict_proba(test_X_scaled)  # Getting probabilities for both labels
            predicted_labels = nn_clf.predict(test_X_scaled)
            # Rank results for label 1 and store document ID with probability
            ranked_samples = []
            for idx, label in enumerate(predicted_labels):
                if label == 1:  # We only care about label 1
                    doc_id = value[idx][0]  # Use the doc_id from the 'value' tuple
                    prob = test_probs[idx][1]  # Probability of label 1.0
                    ranked_samples.append((doc_id, prob))
            # Sort by probability in descending order
            ranked_samples.sort(key=lambda x: x[1], reverse=True)
            test_results[key] = ranked_samples
    ##print(test_results)
    # Save results to a pickle file
    with open("ranked_results.pkl", "wb") as file:
        pickle.dump(test_results, file)
    # Optionally, print the top-ranked results for inspection
    #for key, ranked_samples in test_results.items():
    #    print(f"Results for key {key}:")
    #    for idx, (doc_id, prob) in enumerate(ranked_samples[:10], 1):
    #        print(f"{idx}. Doc ID: {doc_id}, Probability: {prob:.4f}")


def mpnn():
    with open("initRanked.pkl", "rb") as f:
        data_dict = pickle.load(f)
    all_tuples = []
    feature_ids = {
        'text': 1,
        'title': 2,
        'msc': 3,
        'keywords': 4,
        'references': 5
    }
    for feature, feature_id in feature_ids.items():
        feature_data = data_dict.get(feature, [])
        for doc_id, score in feature_data:
            all_tuples.append((feature_id, score))
    # Convert the list of tuples to a numpy array for MLPClassifier
    all_tuples_array = np.array(all_tuples)
    X_data = all_tuples_array[:, 1].reshape(-1, 1)  # Feature: score
    feature_ids = all_tuples_array[:, 0].reshape(-1, 1)  # Feature IDs
    # Combine features (feature_id and score) as input for MLPClassifier
    X_combined = np.hstack((feature_ids, X_data))
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_combined)
    nn_clf = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
    # Predicting probabilities for the test data (labels and probabilities)
    test_probs = nn_clf.predict_proba(X_scaled)  # Getting the probability for label 1.0
    predicted_labels = nn_clf.predict(X_scaled)
    # Store the doc_id, predicted label, and probability (only for label 1.0)
    ranked_samples = []
    for idx, label in enumerate(predicted_labels):
        if label == 1:
            doc_id = data_dict['text'][idx][0]  # Use doc_id from the 'text' feature
            prob = test_probs[idx][1]  # Probability of label 1.0
            ranked_samples.append((doc_id, prob))
    ranked_samples.sort(key=lambda x: x[1], reverse=True)     # Rank the samples based on probability in descending order
    top_10_doc_ids = [doc_id for doc_id, _ in ranked_samples[:10]]
    print("Top 10 Ranked Document IDs:")
    for idx, doc_id in enumerate(top_10_doc_ids, 1):
        print(f"{idx}. {doc_id}")
    with open("ranked_ids.pkl", "wb") as wpf:
        pickle.dump(ranked_samples, wpf)

mpnn()