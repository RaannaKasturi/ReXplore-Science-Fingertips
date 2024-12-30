import threading
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import time

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def luhn_summarizer(text_corpus):
    start_time = time.time()
    parser = PlaintextParser.from_string(text_corpus, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LuhnSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    sentences = summarizer(parser.document, 25)
    summary = ""
    for sentence in sentences:
        summary += str(sentence) + ""
    end_time = time.time()
    print(f"Time taken (Math Summary 1): {end_time - start_time:.2f} seconds")
    return summary

def textrank_summarizer(text_corpus):
    start_time = time.time()
    parser = PlaintextParser.from_string(text_corpus, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    sentences = summarizer(parser.document, 25)
    summary = ""
    for sentence in sentences:
        summary += str(sentence) + ""
    end_time = time.time()
    print(f"Time taken (Math Summary 2): {end_time - start_time:.2f} seconds")
    return summary

def sanitize_text(input_string):
    try:
        encoded_bytes = input_string.encode("utf-8")
        decoded_string = encoded_bytes.decode("utf-8")
        return decoded_string
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        raise
    except UnicodeDecodeError as e:
        print(f"Decoding error: {e}")
        raise

def generate_math_summary(research_paper_text):
    sanitized_text = sanitize_text(research_paper_text)
    try:
        textrank_summary = luhn_summary = lsa_summary = lexrank_summary = None
        def run_textrank():
            nonlocal textrank_summary
            textrank_summary = textrank_summarizer(sanitized_text)
        def run_luhn():
            nonlocal luhn_summary
            luhn_summary = luhn_summarizer(sanitized_text)
        threads = []
        threads.append(threading.Thread(target=run_textrank))
        threads.append(threading.Thread(target=run_luhn))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        math_summary = textrank_summary.replace("\n", "") + luhn_summary.replace("\n", "")
        return math_summary
    except Exception as e:
        print(e)
        return False
    
if __name__ == "__main__":
    research_paper_text = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."
    print(generate_math_summary(research_paper_text))