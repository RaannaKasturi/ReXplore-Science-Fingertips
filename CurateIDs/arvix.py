import json
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import utils
from bs4 import BeautifulSoup

def fetch_new_page(category):
    url = f'https://arxiv.org/list/{category}/new'
    return utils.fetch_page(url)

def fetch_recent_page(category):
    url = f'https://arxiv.org/list/{category}/recent'
    return utils.fetch_page(url)

def extract_new_data(category):
    paper_ids = []
    page_content = fetch_new_page(category)
    lists = BeautifulSoup(page_content, 'html.parser').find_all('dl')
    for list in lists:
        papers = list.find_all('dt')
        paper_contents = list.find_all('dd')
        titles = [paper_content.find('div', class_='list-title').text.strip().split('Title:')[-1].strip() for paper_content in paper_contents]
        for paper, title in zip(papers, titles):
            if not utils.verify_simple_title(title):
                continue
            else:
                paper_link = paper.find('a', href=True)
                if paper_link:
                    paper_id = paper_link.text.strip().split(':')[1]
                    paper_ids.append(paper_id)
                else:
                    continue
    return paper_ids

def extract_recent_data(category):
    paper_ids = []
    page_content = fetch_recent_page(category)
    lists = BeautifulSoup(page_content, 'html.parser').find_all('dl')
    for list in lists:
        papers = list.find_all('dt')
        for paper in papers:
            paper_link = paper.find('a', href=True)
            if paper_link:
                paper_id = paper_link.text.strip().split(':')[1]
                paper_ids.append(paper_id)
            else:
                continue
    return paper_ids

def extract_data(category):
    sanitized_data = []
    new_data = extract_new_data(category)
    recent_data = extract_recent_data(category)
    data = list(set(new_data + recent_data))
    if category in ["hep-ex", "hep-lat", "hep-ph", "hep-th"]:
        category_list = []
        for id in data:
            if len(category_list) >= 1:
                break
            if utils.check_data_in_file(id, 'arxiv.txt'):
                continue
            else:
                category_list.append(id)
        for category_id in category_list:
            sanitized_data.append(category_id)
            utils.write_data_to_file(id, 'arxiv.txt')
    else:
        for id in data:
            if len(sanitized_data) >= 3:
                break
            if utils.check_data_in_file(id, 'arxiv.txt'):
                continue
            else:
                utils.write_data_to_file(id, 'arxiv.txt')
                sanitized_data.append(id)
    random.shuffle(sanitized_data)
    return sanitized_data

def extract_arxiv_data():
    if not utils.download_datafile('arxiv.txt'):
        raise Exception("Failed to download datafile")
    categories = {
        "Astrophysics": ["astro-ph"],
        "Condensed Matter": ["cond-mat"],
        "General Relativity and Quantum Cosmology": ["gr-qc"],
        "High Energy Physics": ["hep-ex", "hep-lat", "hep-ph", "hep-th"],
        "Mathematical Physics": ["math-ph"],
        "Nonlinear Sciences": ["nlin"],
        "Nuclear Experiment": ["nucl-ex"],
        "Nuclear Theory": ["nucl-th"],
        "Physics": ["physics"],
        "Quantum Physics": ["quant-ph"],
        "Mathematics": ["math"],
        "Computer Science": ["cs"],
        "Quantitative Biology": ["q-bio"],
        "Quantitative Finance": ["q-fin"],
        "Statistics": ["stat"],
        "Electrical Engineering and Systems Science": ["eess"],
        "Economics": ["econ"]
    }
    data = {}
    for category, subcategories in categories.items():
        category_data = {}
        all_ids = []
        temp_id_storage = []
        for subcategory in subcategories:
            ids = extract_data(subcategory)
            if len(ids) == 3:
                for id in ids:
                    temp_id_storage.append(id)
            else:
                for id in ids:
                    all_ids.append(id)
        for temp_id in temp_id_storage:
            all_ids.append(temp_id)
        random.shuffle(all_ids)
        if len(all_ids) > 3:
            print(f"Found more than 3 papers for {category}.")
            all_ids = all_ids[:3]
        category_data['count'] = len(all_ids)
        category_data['ids'] = all_ids
        data[category] = category_data
    data = json.dumps(data, indent=4, ensure_ascii=False)
    if not utils.upload_datafile('arxiv.txt'):
        raise Exception("Failed to upload datafile")
    return data

if __name__ == '__main__':
    data = extract_arxiv_data()
    with open('arxiv_data.json', 'w') as f:
        f.write(data)