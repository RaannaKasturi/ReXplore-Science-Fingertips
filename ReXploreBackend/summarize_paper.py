import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from Summarizer.summarizer import generate_summary_mindmap

def summarize_paper(pdf_url, paper_id, access_key):
    mindmap = None
    summary = None
    data = generate_summary_mindmap(pdf_url, paper_id, access_key)
    mindmap = data.get('mindmap')
    summary = data.get('summary')
    return summary, mindmap
