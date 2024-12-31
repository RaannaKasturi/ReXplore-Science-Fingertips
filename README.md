# ReXplore: Science Simplified, Knowledge Amplified [![Check and Schedule Blog Posting](https://github.com/RaannaKasturi/ReXplore-Backend/actions/workflows/main.yml/badge.svg)](https://github.com/RaannaKasturi/ReXplore-Backend/actions/workflows/main.yml)

ReXplore makes the latest scientific research accessible to all.
With clear summaries, detailed insights, and interactive mind maps, it brings you the world’s newest discoveries without the need for extensive reading.
It’s science, simplified and right at your fingertips.

## About ReXplore
- The ReXplore is 90% based on Artificial Intelligence and 10% on traditional Python Programming.
- A ReXplore's LLM Model is a custom trained LLM model based on [Llama 3.1 405B Instruct](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct) and [PMC_MindMap](https://huggingface.co/datasets/raannakasturi/PMC_MindMap).
- The DOI IDs for latest Research Papers Published are fetched from [arXiv](https://arxiv.org/), [ScienceDaily](https://www.sciencedaily.com/) and [HuggingFace's Daily Papers](https://huggingface.co/papers) (Under Development).
- ReXplore has been developed as a Thesis Project with the aim to make general public aware of Research Papers and Latest Development in Scientific Community

# How Does ReXplore Works
1. Fetches arXiv IDs and DOI IDs from source website.
2. Converts all IDs in favourable DOI IDs.
3. Downloads Research Papers for each ID.
4. Extracts and Limits extracted text to certain lines using TextRank and Luhn Algorithms.
5. Processes the text or mathematically summarized content to build suitable LLM prompt.
6. Generated Summary (with Highlights and key Insights) (Markdown Format) and Mindmap (Markdown Format) along with AI-generated images.
7. Creates HTML Template of Summary and Mindmap and also uploads the AI-generated images to Imgbb and fetches most suitable and fastest image link
8. Posts the generated Blog (HTML Format) on Blogger using Blogger API.
9. Notifies Publisher of the Blogs Published via Email.

# Special Thanks
- [Prarthi Kothari](https://github.com/PrarthiKothari) for helping to develop dataset and training LLM model by allowing access to their Systems.
- [Google Blogger (API)](https://developers.google.com/blogger) for extending normal API limits allowing to share more posts.
- Synthetic Lab, Co. (San Francisco, CA 94114) for deploying trained LLM Model and allowing it's private access.
- [SendInBlue](https://www.brevo.com/) for API access to send notifing mails.
- [Pollinations.AI](https://pollinations.ai/) for the access to seamless and unlimited AI-Image generation.
- [Imgbb](https://imgbb.com/) for API access and for image storage facility. 
- [Google Developer Account](https://developer.android.com/distribute/console) (Waiting for funds to proceed).

# Technologies Used
- Python3
- HuggingFace Spaces
- Blogger
- GitHub WorkFlows
- Pollinations.AI
- Imgbb
- Brevo

