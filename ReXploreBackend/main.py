import json
import os
import dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/")
from summarize_paper import summarize_paper
from fetch_data import fetch_paper_data_with_category
from post_blog import post_blog
from send_mail import send_email

# Load environment variables
dotenv.load_dotenv()
access_key = os.getenv("ACCESS_KEY")

def paper_data(paper_data, wait_time=3):
    data = {"status": "success"}
    data['data'] = {}
    paper_data = json.loads(paper_data)
    for category, papers in paper_data.items():
            print(f"Processing category: {category}")
            data['data'][category] = {}
            for paper_id, details in papers.items():
                doi = details.get("doi")
                pdf_url = details.get("pdf_url")
                title = details.get("title")
                citation = details.get("citation")
                if not all([paper_id, doi, pdf_url, title, citation]):
                    print(f"Skipping paper with ID: {paper_id} (missing details)")
                    continue
                summary, mindmap = summarize_paper(pdf_url, paper_id, access_key)
                post_blog(title, category, summary, mindmap, citation, access_key, wait_time)
                data['data'][category][paper_id] = {
                    "id": paper_id,
                    "doi": doi,
                    "title": title,
                    "category": category,
                    "citation": citation,
                    "summary": summary,
                    "mindmap": mindmap,
                }
    data = json.dumps(data, indent=4, ensure_ascii=False)
    return data

def post_blogpost(uaccess_key, wait_time=3):
    if uaccess_key != access_key:
        return False
    data = fetch_paper_data_with_category(uaccess_key)
    pdata = paper_data(data, wait_time)
    try:
        send_email(pdata)
        print("\n-------------------------------------------------------\nMail Sent\n-------------------------------------------------------\n")
    except Exception as e:
        print(f"\n-------------------------------------------------------\nError sending mail: {e}\n-------------------------------------------------------\n")
    finally:
        print("\n-------------------------------------------------------\nProcess Completed\n-------------------------------------------------------\n")
    return pdata