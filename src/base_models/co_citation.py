import sys
import json
import csv
import math
import pickle
import pandas as pd
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from data import offlinedata

csv.field_size_limit(sys.maxsize)
model = SentenceTransformer("dunzhang/stella_en_400M_v5", device='cuda', trust_remote_code=True)
query_prompt_name = "s2p_query"

def getDocID_to_zbl():
    dictRef = dict()
    with open("data/id_to_ZBL.csv", mode ='r') as csvfile:
        csvFile = csv.reader(csvfile)
        first_row = next(csvFile)
        for lines in csvFile:
            dictRef[lines[0]] = lines[1]
    zbl_to_ids = {y: x for x, y in dictRef.items()}
    return dictRef,zbl_to_ids

def getDocandRefstyle():
    dictRef = dict()
    filename = "data/references_withID.csv"
    with open(filename, 'r', encoding="utf-8", errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)  # Read the first row
        for eachro in csvreader:
            dictRef[eachro[2]] = eachro[1]
    return dictRef

def getAllReferences():
    """Combine refrences in ZBL and and normal format"""
    file_zblcit = "data/math_citation.csv"
    file_ref = "data/references_withID.csv"
    idToZBLcit_o = dict()
    with open(file_zblcit, 'r', encoding="utf-8", errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)
        for eachro in csvreader:
            if eachro[1] != "":
                idToZBLcit_o[eachro[0]]=eachro[1]
    idToZBLcit_re = dict()
    for eachD in idToZBLcit_o.keys():
        temp_c = idToZBLcit_o[eachD].split(";")
        temp_cn = list()
        for eachE in temp_c:
            ele_n = eachE.split(" ")
            if "Zbl" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("Zbl")[1]
                temp_cn.append(ele_n)
            elif "JFM" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("JFM")[1]
                temp_cn.append(ele_n)
            elif "ERAM" in ele_n:
                ele_n = "".join(ele_n)
                ele_n = ele_n.split("ERAM")[1]
                temp_cn.append(ele_n)
            else:
                # some IDs start woth "JM" or no identifier or just weird latex form.
                # Upon manually checking these documents had no to very little dataat zbMATH Open
                # Hence ignored for now
                continue
        idToZBLcit_re[eachD] = temp_cn
    #print("The pribt shooooooooo: ",idToZBLcit_o["1262405"])
    idToRefrences_o = defaultdict(lambda: list())
    with open(file_ref, 'r', encoding="utf-8", errors='ignore') as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = next(csvreader)
        for eachro in csvreader:
            if eachro[2] != "":
                idToRefrences_o[eachro[0]].append([eachro[1],eachro[2]])
    getExistingDEtoRefStyle = getDocandRefstyle()
    for eachID in idToZBLcit_re.keys():
        if eachID in idToRefrences_o.keys():
            listOfpresentZBL = [ele[1] for ele in idToRefrences_o[eachID]]
            for eachZBL in idToZBLcit_re[eachID]:
                if eachZBL not in listOfpresentZBL:
                    if eachZBL in getExistingDEtoRefStyle.keys():
                        idToRefrences_o[eachID].append([getExistingDEtoRefStyle[eachZBL], eachZBL])
        else:
            for eachZBL in idToZBLcit_re[eachID]:
                if eachZBL in getExistingDEtoRefStyle.keys():
                    idToRefrences_o[eachID].append([getExistingDEtoRefStyle[eachZBL], eachZBL])
    return idToRefrences_o

def getRefSimilaritySplit():
    train, test, val = offlinedata.getdata()
    id_toRefrences = getAllReferences()
    zbl_to_ids,ids_to_zbl = getDocID_to_zbl()
    getDocref = getDocandRefstyle()
    IniTrefcs = {}
    for index, row in test.iterrows():
        doc_id = str(row['document_id'])
        listGenrec = []
        print("doing for document: ", doc_id, flush=True)
        if doc_id in ids_to_zbl.keys():
            if ids_to_zbl[doc_id] in getDocref.keys():
                if doc_id in id_toRefrences.keys():
                    seed_str = getDocref[ids_to_zbl[doc_id]]
                    #print("Seed str: ", seed_str)
                    rfrncs = id_toRefrences[doc_id]
                    query_embeddings = model.encode([seed_str], prompt_name=query_prompt_name)
                    doc_embeddings = model.encode([el[0] for el in rfrncs])
                    docIds = [zbl_to_ids[el[1]] if el[1] in zbl_to_ids.keys() else '111' for el in rfrncs]
                    similarities = model.similarity(query_embeddings, doc_embeddings)
                    for ids_, eachScr in enumerate(similarities[0]):
                        listGenrec.append([int(docIds[ids_]), eachScr])
                    listGenrec = sorted(listGenrec, key=lambda x: float(x[1]), reverse=True)
        IniTrefcs[doc_id] = listGenrec
    with open('initRanked_refs.pkl', 'wb') as file:
        pickle.dump(IniTrefcs, file)

getRefSimilaritySplit()