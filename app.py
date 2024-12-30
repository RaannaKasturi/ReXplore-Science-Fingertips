import gradio as gr
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from ReXploreBackend.main import post_blogpost
from ReXploreBackend.post_blog import test
from env_variables_setup import setup_application

theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[
        gr.themes.GoogleFont("Syne"), 
        gr.themes.GoogleFont("Poppins"), 
        gr.themes.GoogleFont("Poppins"), 
        gr.themes.GoogleFont("Poppins")
    ],
)

with gr.Blocks(theme=theme, title="ReXplore Backend", fill_height=True) as app:
    gr.HTML(
        value ="""
        <h1 style="text-align: center;">ReXplore Backend<p style="text-align: center;">Designed and Developed by <a href="https://raannakasturi.eu.org" target="_blank" rel="nofollow noreferrer external">Nayan Kasturi</a></p> </h1>
        <p style="text-align: center;">Backend for ReXplore</p>
        """)
    with gr.Row():
        with gr.Column():
            with gr.Row():
                access_key = gr.Textbox(label="Access Key", placeholder="Enter the Access Key", type="password")
                wait_time = gr.Number(value=5, minimum=3, maximum=15, step=1, label="Wait Time", interactive=True)
            with gr.Row():
                start = gr.Button(value="Start", variant="primary")
                test_btn = gr.Button(value="Test", variant="secondary")
        status = gr.Textbox(label="Data", placeholder="Enter the data", lines=7)
    start.click(
        post_blogpost,
        inputs=[access_key],
        outputs=[status],
        concurrency_limit=25,
        scroll_to_output=True,
        show_api=True,
        api_name="rexplore_backend",
        show_progress="full",
    )
    test_btn.click(test,
        inputs=[access_key],
        outputs=[status],
        concurrency_limit=25,
        scroll_to_output=True,
        show_api=True,
        api_name="rexplore_backend_test",
        show_progress="full")

if __name__ == "__main__":
    try:
        import shutil
        shutil.rmtree("downloads")
    except Exception as e:
        print(e)
    finally:
        os.mkdir("downloads")
    if setup_application():
        app.queue(default_concurrency_limit=25).launch(show_api=True, show_error=True, debug=True, inbrowser=True)
    else:
        print("Error setting up application")