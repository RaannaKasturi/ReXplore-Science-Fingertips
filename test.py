import os
import dotenv
from gradio_client import Client
from concurrent.futures import ThreadPoolExecutor, TimeoutError

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
    result = client.predict(
        uaccess_key=access_key,
        api_name="/rexplore_backend"
    )
    return result

def execute_with_timeout(func, timeout):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            return None
        except Exception as e:
            print(f"Function {func.__name__} raised an exception: {e}")
            return None

def main():
    if not access_key:
        raise ValueError("ACCESS_KEY is not set in the environment variables.")
    test_result = test()
    print(f"test() returned: {test_result}")
    if not test_result:
        raise RuntimeError("API test function failed or returned an invalid response.")
    post_blogs_result = execute_with_timeout(post_blogs, timeout=20)
    if post_blogs_result is None:
        print("post_blogs() timed out or failed to execute.")
    else:
        print(f"post_blogs() returned: {post_blogs_result}")
    return test_result

if __name__ == "__main__":
    main_result = main()
    print(f"Final result: {main_result}")
