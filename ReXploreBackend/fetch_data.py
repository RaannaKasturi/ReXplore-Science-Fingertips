import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from CurateIDs.fetch_ids import fetch_ids
from CurateData.fetch_data import fetch_paper_data

def fetch_category_ids(uaccess_key):
    """Fetch category IDs using the category API."""
    if not uaccess_key:
        raise ValueError("API access key not found. Please check your environment variables.")
    try:
        result = fetch_ids(uaccess_key)
        cat_ids = json.loads(result)
        if cat_ids['status'] == 'success':
            return cat_ids['data']
        else:
            return None
    except Exception as e:
        print(f"Exception while fetching category IDs: {str(e)}")
        return None

def fetch_single_paper_data(paper_id):
    try:
        result = fetch_paper_data(paper_id)
        paper_data = json.loads(result)
        if paper_data['status'] == 'success':
            return paper_id, paper_data['data']
        else:
            print(f"Failed to fetch data for paper ID {paper_id}: {paper_data.get('message', 'Unknown error')}")
            return paper_id, None
    except Exception as e:
        print(f"Exception while fetching data for paper ID {paper_id}: {str(e)}")
        return paper_id, None

def fetch_paper_data_concurrently(paper_ids, max_threads=12):
    paper_id_data = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_paper_id = {executor.submit(fetch_single_paper_data, paper_id): paper_id for paper_id in paper_ids}
        for future in as_completed(future_to_paper_id):
            paper_id = future_to_paper_id[future]
            try:
                paper_id, data = future.result()
                if data:
                    paper_id_data[paper_id] = data
            except Exception as e:
                print(f"Error fetching data for paper ID {paper_id}: {str(e)}")
    return paper_id_data

def fetch_paper_data_with_category(cat_ids_api_key):
    data = {}
    try:
        cat_ids = fetch_category_ids(cat_ids_api_key)
        if cat_ids:
            for category, ids in cat_ids.items():
                print(f"Fetching data for category: {category}")
                try:
                    paper_data = fetch_paper_data_concurrently(ids['ids'])
                    if paper_data:
                        data[category] = paper_data
                except Exception as e:
                    print(f"Error fetching data for category {category}: {str(e)}")
                    continue
        return json.dumps(data, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Exception while fetching paper data by category: {str(e)}")
        return None
