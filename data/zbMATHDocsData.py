import sys
import requests
import pandas as pd
import xml.etree.ElementTree as ET

def fetch_zbmath_records():
    base_url = "https://oai.zbmath.org/?verb=ListRecords&metadataPrefix=oai_dc"
    records = []
    while base_url:
        print(f"Fetching: {base_url}")
        response = requests.get(base_url)
        if response.status_code != 200:
            print("Error fetching data.")
            break
        root = ET.fromstring(response.text)
        # Extract records
        for record in root.findall(".//{http://www.openarchives.org/OAI/2.0/}record"):
            records.append(ET.tostring(record, encoding="utf-8").decode("utf-8"))
        # Check for resumptionToken (to get more records)
        token_elem = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
        if token_elem is not None and token_elem.text:
            base_url = f"https://oai.zbmath.org/?verb=ListRecords&metadataPrefix=oai_dc&resumptionToken={token_elem.text}"
        else:
            base_url = None
    print(f"Total records fetched: {len(records)}")
    return records

def parse_zbmath_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for record in root.findall(".//{/OAI/2.0/}record"):
        document_id = record.find(".//{/1.1/}_id")
        msc = record.find(".//{/1.1/}classification")
        keywords = record.find(".//{/1.1/}keywords")
        title = record.find(".//{/1.1/}title")
        review = record.find(".//{/1.1/}reviewtext")
        references = record.find(".//{/1.1/}references")
        data.append({
            "document_id": document_id.text if document_id is not None else "N/A",
            "title": title.text if title is not None else "N/A",
            "review": review.text if review is not None else "N/A",
            "msc": msc.text if msc is not None else "N/A",
            "keywords": keywords.text if keywords is not None else "N/A",
            "references": references.text if references is not None else "N/A",
            "references_id": references.ref_id if references is not None else "N/A",
        })
    df = pd.DataFrame(data)
    df.to_csv("zbmath_data.csv", index=False)

records = fetch_zbmath_records()
with open("zbmath_records.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(records))
parse_zbmath_xml("zbmath_records.xml")