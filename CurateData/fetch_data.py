import re
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/131.0.6778.135 Safari/537.36'
}

def fetch_pmc_doi(pmc_id):
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?email=raannakasturi@gmail.com&ids={pmc_id}&format=json"
    response = requests.get(url, headers=HEADERS).json()
    if response['status'] == 'ok':
        doi = response['records'][0]['doi']
        return f"https://doi.org/{doi}"

def fetch_pmc_pdf(pmc_id):
    pdf_url = None
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmc_id}&format=pdf"
    response = requests.get(url, headers=HEADERS).content
    try:
        ET.fromstring(response).find(".//error").text
        url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc_id}/"
        response = requests.get(url, headers=HEADERS).content
        data = BeautifulSoup(response, 'html.parser')
        pdf_url = data.find("a", {"data-ga-label" : "pdf_download_desktop"}, href=True)
        if pdf_url:
            pdf_url = url + pdf_url['href']
        else:
            return None
    except Exception as e:
        pdf_url = ET.fromstring(response).find("records").find("record").find("link").attrib['href'].replace('ftp://', 'http://')
    finally:
        return pdf_url

def fetch_arxiv_doi(arxiv_id):
    page_url = f"https://arxiv.org/abs/{arxiv_id}"
    page_content = requests.get(page_url, headers=HEADERS).content
    page_data = BeautifulSoup(page_content, 'html.parser')
    doi = page_data.find('td', {'class': "tablecell arxivdoi"}).find('a', {'id': 'arxiv-doi-link'}).text
    return doi

def fetch_citation(doi):
    url = f"https://citation.crosscite.org/format?doi={doi}&style=apa&lang=en-US"
    headers = {
        "accept": "text/plain, */*; q=0.01",
        "accept-language": "en-US,en-GB;q=0.9,en;q=0.8",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "Referer": "https://citation.crosscite.org/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()

def fetch_title(doi):
    title_content = requests.get(doi, headers={ 'User-Agent':HEADERS['User-Agent'], 'Accept': 'text/x-bibliography; style=bibtex'}).content
    bibtex_entry = title_content.decode('utf-8').strip()
    title = re.search(r'title\s*=\s*{(.*?)}', bibtex_entry)
    if title:
        return title.group(1).strip()
    return None

def fetch_paper_data(id):
    data = {}
    try:
        if id.startswith('PMC'):
            doi = fetch_pmc_doi(id)
            pdf_url = fetch_pmc_pdf(id)
        else:
            doi = fetch_arxiv_doi(id)
            pdf_url = f"https://arxiv.org/pdf/{id}"
        if doi and pdf_url:
            citation = fetch_citation(doi).replace('\n', ' ').replace("<i>", "").replace("</i>", "").strip()
            title = fetch_title(doi).replace('\n', ' ').strip()
            data['status'] = 'success'
            data['data'] = {}
            data['data']['doi'] = doi
            data['data']['title'] = title
            data['data']['pdf_url'] = pdf_url
            data['data']['citation'] = citation
    except Exception as e:
        data['status'] = 'error'
        print(str(e))
    return json.dumps(data, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    data = fetch_paper_data('PMC5334499')
    print(data)
