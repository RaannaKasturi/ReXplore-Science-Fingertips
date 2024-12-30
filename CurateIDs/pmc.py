import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import utils
import threading

def fetch_links(category):
    links = []
    xml_data = utils.fetch_page(f"https://www.sciencedaily.com/rss/top/{category.lower()}.xml")
    items = ET.fromstring(xml_data).findall('channel/item')
    for item in items:
        link = item.find('link').text
        links.append(link)
    return links

def fetch_all_links():
    categories = ["Science", "Health", "Environment", "Technology", "Society"]
    sd_links_data = {}
    for category in categories:
        links = fetch_links(category)
        sd_links_data[category] = links
    data = json.dumps(sd_links_data, indent=4, ensure_ascii=False)
    return data

def fetch_dois():
    doi_data = {}
    data = json.loads(fetch_all_links())
    for topic, links in data.items():
        doi_list = []
        for link in links:
            page_content = utils.fetch_page(link)
            page_datas = BeautifulSoup(page_content, 'html.parser').find_all("div", id="journal_references")
            for page_data in page_datas:
                if not page_data.find("a", href=True):
                    continue
                else:
                    doi = page_data.find("a", href=True).text
                    if doi.startswith('10.'):
                        doi_list.append(doi)
                    else:
                        continue
        doi_data[topic] = doi_list
    data = json.dumps(doi_data, indent=4, ensure_ascii=False)
    return data

def fetch_doi_data():
    result = []
    def fetch_and_store():
        result.append(fetch_dois())
    thread = threading.Thread(target=fetch_and_store)
    thread.start()
    thread.join()
    if len(result) == 0 or not result or result[0] == None:
        return []
    return result[0]

def doi_to_pmc():
    data = json.loads(fetch_doi_data())
    pmc_data = {}
    for topic, dois in data.items():
        if len(dois) > 0:
            doi_list = ""
            for doi in dois:
                doi_list += doi + ","
            doi_list = doi_list.rstrip(',')
            try:
                url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?email=raannakasturi@gmail.com&ids={doi_list}&format=json"
                doi_pmc_data = requests.get(url).json()
            except Exception as e:
                print(f"Error: {str(e)}")
            if doi_pmc_data['status'] == 'ok':
                pmc_list = []
                for record in doi_pmc_data['records']:
                    if 'pmcid' in record:
                        if 'live' in record and record['live'] == False:
                            continue
                        pmc_list.append(record['pmcid'])
                    else:
                        continue
                pmc_data[topic] = pmc_list
            else:
                continue
        else:
            continue
    data = json.dumps(pmc_data, indent=4, ensure_ascii=False)
    return data

def extract_pmc_data():
    if not utils.download_datafile('pmc.txt'):
        raise Exception("Failed to download datafile")
    pmc_data ={}
    pmcid_data = json.loads(doi_to_pmc())
    for topic, pmcids in pmcid_data.items():
        pmc_ids = []
        for id in pmcids:
            if len(pmc_ids) >= 3:
                continue
            elif utils.check_data_in_file(id, 'pmc.txt'):
                continue
            else:
                utils.write_data_to_file(id, 'pmc.txt')
                pmc_ids.append(id)
        pmc_data[topic] = {}
        pmc_data[topic]['count'] = len(pmc_ids)
        pmc_data[topic]['ids'] = pmc_ids
    data = json.dumps(pmc_data, indent=4, ensure_ascii=False)
    if not utils.upload_datafile('pmc.txt'):
        raise Exception("Failed to upload datafile")
    return data

if __name__ == "__main__":
    data = extract_pmc_data()
    with open('pmc_data.json', 'w') as f:
        f.write(data)