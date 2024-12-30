from pdfplumber import open as pdf_open
import requests
import os
import requests
import re
import os
import dotenv
from huggingface_hub import HfApi

dotenv.load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")
access_key = os.getenv("ACCESS_KEY")

def download_pdf(url, id):
    id = id.replace("/", "-")
    directory = "downloads"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{id}.pdf")
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"})
        response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None
    return file_path

def extract_text_from_pdf(url, id):
    pdf_path = download_pdf(url, id)
    try:
        with pdf_open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() + " "
        start_index = all_text.find("ABSTRACT")
        end_index = all_text.find("REFERENCES")
        if start_index != -1 and end_index != -1 and start_index < end_index:
            relevant_text = all_text[start_index:end_index]
        else:
            relevant_text = all_text
        research_paper_text = relevant_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        research_paper_text = ""
    finally:
        os.remove(pdf_path)
    return research_paper_text

def fetch_page(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/131.0.6778.135 Safari/537.36'
    }
    page_content = requests.get(url, headers=HEADERS).content
    return page_content

def check_data_in_file(data, file):
    with open(file, 'r') as f:
        existing_data = f.read().splitlines()
    if data in existing_data:
        return True
    else:
        return False
    
def write_data_to_file(data, file):
    with open(file, 'a') as f:
        f.write(data + '\n')
    return True

def verify_simple_title(title):
    pattern = re.compile(r'^[a-zA-Z0-9\s\.\-\+\*/=\(\)\[\]\{\},:;"\'?\>\<\@\#\%\^\*\|\_\~\`]+$')
    if pattern.match(title):
        return True
    else:
        return False
    
def download_datafile(filename):
    try:
        api = HfApi(token=hf_token)
        api.hf_hub_download(repo_id="raannakasturi/ReXploreData", filename=filename, repo_type="dataset", local_dir='.', cache_dir='.', force_download=True)
        return True
    except Exception as e:
        print(str(e))
        return False

def upload_datafile(filename):
    try:
        api = HfApi(token=hf_token)
        api.upload_file(path_or_fileobj=filename, path_in_repo=filename, repo_id="raannakasturi/ReXploreData", repo_type="dataset")
        os.remove(filename)
        return True
    except Exception as e:
        print(str(e))
        return False
    
def reset_datafiles(user_access_key):
    if user_access_key != access_key:
        return "Invalid access key"
    else:
        files  = ['arxiv.txt', 'pmc.txt']
        try:
            for filename in files:
                try:
                    download_datafile(filename)
                    with open(filename, 'w') as f:
                        f.write('')
                    upload_datafile(filename)
                except Exception as e:
                    print(str(e))
                    continue
            return True
        except Exception as e:
            print(str(e))
            return False

def fetch_page(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/131.0.6778.135 Safari/537.36'
    }
    page_content = requests.get(url, headers=HEADERS).content
    return page_content
