import threading
import os
import dotenv
from gradio_client import Client

dotenv.load_dotenv()
access_key = os.getenv("ACCESS_KEY")

def test():
    client = Client("raannakasturi/ReXploreBackend")
    result = client.predict(
            uaccess_key=access_key,
            api_name="/rexplore_backend_test"
    )
    return result

def post_blogs():
    client = Client("raannakasturi/ReXploreBackend")
    print("Starting to Posting blogs...")
    result = client.predict(
            uaccess_key=access_key,
            api_name="/rexplore_backend"
    )
    print(f"Blog Posting Started")

def fire_and_forget(func):
    thread = threading.Thread(target=func, daemon=True)  # Set daemon=True
    thread.start()

def main():
    if not access_key:
        raise ValueError("ACCESS_KEY is not set in the environment variables.")
    test_result = test()
    print(f"test() returned: {test_result}")
    if not test_result:
        raise RuntimeError("API test function failed or returned an invalid response.")
    else:
        print("API test function passed.")
        fire_and_forget(post_blogs)
        print("Post blogs triggered and not waiting for response.")
    return test_result

if __name__ == "__main__":
    main_result = main()
    print(f"Final result: {main_result}")
