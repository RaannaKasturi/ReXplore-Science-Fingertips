import json
import dotenv
from concurrent.futures import ThreadPoolExecutor
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from CurateIDs.arvix import extract_arxiv_data
from CurateIDs.pmc import extract_pmc_data

dotenv.load_dotenv()
access_key = os.getenv("ACCESS_KEY")

def fetch_arxiv_data():
    return json.loads(extract_arxiv_data())

def fetch_pmc_data():
    return json.loads(extract_pmc_data())

def fetch_ids(user_access_key):
    if user_access_key != access_key:
        papers_data = {"status": "Invalid access key"}
    else:
        papers_data = {}
        try:
            papers_data['status'] = 'success'
            papers_data['data'] = {}
            with ThreadPoolExecutor() as executor:
                pmc_future = executor.submit(fetch_pmc_data)
                arxiv_future = executor.submit(fetch_arxiv_data)
                pmc_data = pmc_future.result()
                arxiv_data = arxiv_future.result()
            for topic, topic_data in pmc_data.items():
                if topic_data['count'] == 0:
                    continue
                else:
                    papers_data['data'][topic] = {}
                    papers_data['data'][topic]['ids'] = topic_data['ids']
            for topic, topic_data in arxiv_data.items():
                if topic_data['count'] == 0:
                    continue
                else:
                    papers_data['data'][topic] = {}
                    papers_data['data'][topic]['ids'] = topic_data['ids']
        except Exception as e:
            print(str(e))
            papers_data['status'] = 'error'
    data = json.dumps(papers_data, indent=4, ensure_ascii=False)
    return data

if __name__ == '__main__':
    data = fetch_ids(access_key)
    with open('data.json', 'w') as f:
        f.write(data)