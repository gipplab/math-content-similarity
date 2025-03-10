import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

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