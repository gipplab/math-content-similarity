import re
import sys
import csv
import time
import requests
import pandas as pd
import xml.etree.ElementTree as ET

# Base URL for fetching zbMATH Open document IDs
BASE_URL = "https://oai.zbmath.org/v1/?verb=ListIdentifiers&metadataPrefix=oai_dc"

def getzbDocIDs():
    all_records = []
    resumption_token = None
    while True:
        url = f"{BASE_URL}&resumptionToken={resumption_token}" if resumption_token else BASE_URL
        print(f"Fetching data from: {url}")
        response = requests.get(url) # Send the request
        if response.status_code != 200:
            print(f"Error: Received response code {response.status_code}")
            break
        root = ET.fromstring(response.content) # Parse the XML response
        # Extract identifier values
        for identifier in root.findall(".//{http://www.openarchives.org/OAI/2.0/}identifier"):
            match = re.search(r"oai:zbmath.org:(\d+)", identifier.text)
            if match:
                all_records.append(match.group(1))  # Extract only the numerical part
        # Check for resumptionToken to fetch the next batch
        resumption_token_element = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
        if resumption_token_element is not None and resumption_token_element.text:
            resumption_token = resumption_token_element.text.strip()
            time.sleep(1)  # Sleep to avoid overwhelming the server
        else:
            break  # No more data to fetch
    print(f"Total records fetched: {len(all_records)}")
    return all_records


# URL for fetching document data
BASE_URL = "https://oai.zbmath.org/v1/?verb=GetRecord&identifier=oai:zbmath.org:{}&metadataPrefix=oai_zb_preview"

# Function to fetch document details
def fetch_document_data(doc_id):
    url = BASE_URL.format(doc_id)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {doc_id}. HTTP Status: {response.status_code}")
        return None
    root = ET.fromstring(response.content) # Parse XML response with proper namespaces
    # Define the namespaces
    namespaces = {
        "oai": "http://www.openarchives.org/OAI/2.0/",
        "zbmath": "https://zbmath.org/oai/"
    }
    metadata_node = root.find(".//oai:GetRecord/oai:record/oai:metadata/zbmath:zbmath", namespaces)
    if metadata_node is None:
        print(f"No metadata found for document {doc_id}")
        return None
    document_id = doc_id
    title = metadata_node.find("zbmath:document_title", namespaces)
    title = title.text.strip() if title is not None else ""
    text = metadata_node.find("zbmath:review/zbmath:review_text", namespaces)
    text = text.text.strip() if text is not None else ""
    msc_list = [msc.text.strip() for msc in metadata_node.findall("zbmath:classifications/zbmath:classification", namespaces)]
    keywords_list = [kw.text.strip() for kw in metadata_node.findall("zbmath:keywords/zbmath:keyword", namespaces)]
    keywords = "; ".join(keywords_list) if keywords_list else ""
    references = [ref.find("zbmath:text", namespaces).text.strip() for ref in metadata_node.findall("zbmath:references/zbmath:reference", namespaces) if ref.find("zbmath:text", namespaces) is not None]
    references_id = [ref.find("zbmath:ref_id", namespaces).text.strip() for ref in metadata_node.findall("zbmath:references/zbmath:reference", namespaces) if ref.find("zbmath:ref_id", namespaces) is not None]

    return {
        "document_id": document_id,
        "title": title,
        "text": text,
        "msc": "; ".join(msc_list),
        "keywords": keywords,
        "references": "; ".join(references),
        "references_id": "; ".join(references_id)
    }

# # Fetch data for a specific document
# doc_id = "5797851"
# document_data = fetch_document_data(doc_id)

# Save data to CSV
csv_filename = "zbMATHDocsData.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["document_id", "title", "text", "msc", "keywords", "references", "references_id"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    allZbIDs = getzbDocIDs()
    for eachID in allZbIDs:
        document_data = fetch_document_data(eachID)
        writer.writerow(document_data)

print(f"Data successfully saved to {csv_filename}")