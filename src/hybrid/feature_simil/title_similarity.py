import os
import sys
import csv
import torch
import random
import itertools
import pickle
from collections import defaultdict
from transformers import AutoTokenizer, AutoModel
csv.field_size_limit(100000000)

INSTRUCTIONS = {
    "qa": {
        "query": "Represent this query for retrieving relevant documents: ",
        "key": "Represent this document for retrieval: ",
    }
}

def getidealrecommendations():
    listDocs = list()
    with open("/beegfs/schubotz/ankit/data/recommendationPairs.csv", mode ='r') as csvfile:
        csvFile = csv.reader(csvfile)
        for lines in csvFile:
            IdsandRec = list(filter(None, lines))
            listDocs+= IdsandRec[1:]
    return listDocs

def getSEEDIds():
    """
    get seed IDS in a list
    """
    listDocs = list()
    with open("/beegfs/schubotz/ankit/data/recommendationPairs.csv", mode ='r') as csvfile:
        csvFile = csv.reader(csvfile)
        for lines in csvFile:
            IdsandRec = list(filter(None, lines))
            listDocs.append(IdsandRec[0])
    return listDocs

def getIDs41():
    filename = "/beegfs/schubotz/noah/arxMLiv/zbmath_abstracts.csv"
    dataWhole = list()
    with open(filename, 'r', encoding="utf-8", errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)  # Read the first row
        for eachro in csvreader:
            present14 = False
            for eachmsc in eachro[1].split():
                if "14" == eachmsc[:2]:
                    present14 = True
            if present14:
                dataWhole.append(eachro[0])
    combinedlist = list(set(dataWhole).union(getidealrecommendations()))
    return combinedlist

def getAlltitles(filename):
    """ retrurns dict with key as zbMATH ID and value as titles"""
    dataWhole = dict()
    # impIDs = getIDs41() #Only for 14
    with open(filename, 'r', encoding="utf-8", errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)
        for eachro in csvreader:
            dataWhole[eachro[0]]= eachro[1]
    # main_ids = dict()
    # for each_i in impIDs:
        # try:
            # main_ids[each_i] = dataWhole[each_i]
        # except:
            # print("Not found: ",each_i)
    # return main_ids
    return  dataWhole


def genEmbeddingsBatch():
    alltitles = getAlltitles('/beegfs/schubotz/ankit/data/zbMATH_titles.csv')
    instruction = INSTRUCTIONS["qa"]
    tokenizer = AutoTokenizer.from_pretrained('BAAI/llm-embedder')
    model = AutoModel.from_pretrained('BAAI/llm-embedder')
    queries = [instruction["query"] + alltitles[query] for query in getSEEDIds()]
    query_inputs = tokenizer(queries, padding=True,truncation=True, return_tensors='pt')
    for i in range(0, len(alltitles)-1, 5000):
        print("Doing for batch: ", i)
        keys = [instruction["key"] + alltitles[key] for key in list(alltitles.keys())[i:i+5000]]
        key_inputs = tokenizer(keys, padding=True,truncation=True, return_tensors='pt')
        with torch.no_grad():
            query_outputs = model(**query_inputs)
            key_outputs = model(**key_inputs)
            query_embeddings = query_outputs.last_hidden_state[:, 0]
            key_embeddings = key_outputs.last_hidden_state[:, 0]
            query_embeddings = torch.nn.functional.normalize(query_embeddings, p=2, dim=1)
            key_embeddings = torch.nn.functional.normalize(key_embeddings, p=2, dim=1)
        similarity = query_embeddings @ key_embeddings.T

        with open('data_ne/titles/tit_'+str(i)+'_.pkl', 'wb') as f:
            pickle.dump(similarity,f)

def createDictScores(dir_here):
    alltitles = getAlltitles('/beegfs/schubotz/ankit/data/zbMATH_titles.csv')
    getAllscores = os.listdir(dir_here)
    allSeeds = getSEEDIds()
    # print(getAllscores)
    seed_to_scores = defaultdict(lambda:list())
    for pick in getAllscores:
        with open(os.path.join(dir_here, pick), 'rb') as f:
            scores = pickle.load(f)
        for id_,ele in enumerate(scores):
            seed_to_scores[id_] += ele
    # print(len(seed_to_scores[id_]))
    docIds = list()
    for i in range(0, len(alltitles)-1, 5000):
        docIds += list(alltitles.keys())[i:i+5000]
    # print(len(docIds))
    dictSeedRec = dict()
    for seed in seed_to_scores.keys():
        dictOfscores = dict()
        for id_h, eachScore in enumerate(seed_to_scores[seed]):
            dictOfscores = dict()
            for id_h, eachScore in enumerate(seed_to_scores[seed]):
                dictOfscores[docIds[id_h]] = eachScore.item()
        dictSeedRec[allSeeds[seed]] = dictOfscores
    sorted_dict = dict()
    for each_ in dictSeedRec.keys():
        sorted_dict[each_] = sorted(dictSeedRec[each_].items(), key=lambda x: x[1], reverse=True)
    with open('titles_LLMemb.pkl', 'wb') as f:
        pickle.dump(sorted_dict, f)

createDictScores("/beegfs/schubotz/ankit/code/evaluation/hybridApproach/data_ne/titles")
#getIDs41()
#genEmbeddingsBatch()