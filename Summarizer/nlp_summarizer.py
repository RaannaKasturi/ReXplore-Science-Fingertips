import threading

def generate_nlp_summary(client, temp_summary):
    try:
        completion = client.chat.completions.create(
            model="hf:meta-llama/Meta-Llama-3.1-405B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant for generating well-formatted summaries from scientific research papers."},
                {"role": "user", "content": f'As a text script expert, please help me to write a short text script with the topic \" {temp_summary}\".You have three tasks, which are:\\n    1.to summarize the text I provided into a Summary .Please answer within 150-300 characters.\\n    2.to summarize the text I provided, using up to seven Highlight.\\n    3.to summarize the text I provided, using up to seven Key Insights. Each insight should include a brief in-depth analysis. Key Insight should not include timestamps.\\n    Your output should use the following template strictly, provide the results for the three tasks:\\n    ## Summary\\n    ## Highlights\\n    - Highlights\\n    ## Key Insights\\n    - Key Insights .\\n  Importantly your output must use language \"English\"'}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return False

def generate_nlp_mindmap(client, temp_summary):
    try:
        completion = client.chat.completions.create(
            model="hf:meta-llama/Meta-Llama-3.1-405B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant for generating well-formatted mindmaps from scientific research papers."},
                {"role": "user", "content": f'As a text script expert, please help me to write a short text script with the topic \"{temp_summary}\".Your output should use the following template:\\n\\n## {{Subtitle01}}\\n- {{Bulletpoint01}}\\n- {{Bulletpoint02}}\\n## {{Subtitle02}}\\n- {{Bulletpoint03}}\\n- {{Bulletpoint04}}\\n\\nSummarize the giving topic to generate a mind map (as many subtitles as possible, with a minimum of three subtitles) structure markdown. Do not include anything in the response, that is not the part of mindmap.\\n  Most Importantly your output must use language \"English\" and each point or pointer should include no more than 9 words.'}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return False

def generate_nlp_summary_and_mindmap(client, temp_summary):
    response = {}
    def local_generate_nlp_summary():
        nlp_summary = generate_nlp_summary(client, temp_summary)
        if not nlp_summary:
            response["summary_status"] = "error"
            response["summary"] = None
        else:
            response["summary_status"] = "success"
            response["summary"] = nlp_summary
    def local_generate_nlp_mindmap():
        nlp_mindmap = generate_nlp_mindmap(client, temp_summary)
        if not nlp_mindmap:
            response["mindmap_status"] = "error"
            response["mindmap"] = None
        else:
            response["mindmap_status"] = "success"
            response["mindmap"] = nlp_mindmap
    threads = []
    threads.append(threading.Thread(target=local_generate_nlp_summary))
    threads.append(threading.Thread(target=local_generate_nlp_mindmap))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return response