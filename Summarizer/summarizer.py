import openai
import dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from  Summarizer.math_summarizer import generate_math_summary
from Summarizer.nlp_summarizer import generate_nlp_summary_and_mindmap
from utils import extract_text_from_pdf

dotenv.load_dotenv()
nlp_api_key = os.getenv("NLP_API_KEY")
base_nlp_url = os.getenv("BASE_NLP_URL")
access_key = os.getenv("ACCESS_KEY")

def create_client():
    client = openai.OpenAI(
        api_key=nlp_api_key,
        base_url=base_nlp_url,
    )
    return client

def generate_summary(client, corpus):
    response = {}
    math_summary = generate_math_summary(corpus)
    if not math_summary:
        print("Error generating Math Summary")
        response["summary_status"] = "error"
        response["summary"] = None
        response["mindmap_status"] = "error"
        response["mindmap"] = None
        return response
    else:
        response = generate_nlp_summary_and_mindmap(client, corpus)
        return response

def generate_summary_mindmap(pdf_url, doi, uaccess_key):
    if uaccess_key != access_key:
        return {"error": "Invalid Access Key", "summary": None, "mindmap": None}
    else:
        corpus = extract_text_from_pdf(pdf_url, doi)
        client = create_client()
        response = generate_summary(client, corpus)
        return response
    
if __name__ == "__main__":
    pdf_url = "https://arxiv.org/pdf/2109.10241.pdf"
    doi = "10.1145/3472716.3472831"
    uaccess = "test_access_key"
    print(generate_summary_mindmap(pdf_url, doi, uaccess))