import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle

def LogisticRegressionModel(): 
    train, test, val = offlinedata.getdata()
    data_dict = getLabelledData("data/results/initRanker/validation_s/", val)
    test_dict = getLabelledData("data/results/initRanker/test_s/", test)
    print("len of train and test", len(train), len(test))
    # Prepare training data (score, feat_id) with label
    train_X = []  # Features (score, feat_id)
    train_y = []  # Labels
    for key, value in train_data:
        for doc_id, score, feat_id, label in value:
            train_X.append([score, feat_id])
            train_y.append(label)
    train_X = np.array(train_X)
    train_y = np.array(train_y)
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(train_X)
    # Initialize and train the Logistic Regression model
    logreg_clf = LogisticRegression(max_iter=1000, random_state=42)
    logreg_clf.fit(X_scaled, train_y)
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
            test_probs = logreg_clf.predict_proba(test_X_scaled)  # Getting probabilities for both labels
            predicted_labels = logreg_clf.predict(test_X_scaled)
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
    # Save results to a pickle file
    with open("ranked_results.pkl", "wb") as file:
        pickle.dump(test_results, file)
