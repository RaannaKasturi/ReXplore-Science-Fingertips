import os
import dotenv
import requests

dotenv.load_dotenv()
access_key = os.getenv("ACCESS_KEY")

API_ENDPOINT = "https://raannakasturi-rexplorebackend.hf.space/gradio_api/call/rexplore_backend"
def make_request(data: list[str], proxy: str = None) -> None:
    payload = {"data": data}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        with requests.Session() as session:
            response = session.post(API_ENDPOINT, json=payload, proxies=proxies)
            if response.status_code != 200:
                raise Exception(f"POST request failed with status {response.status_code}: {response.text}")
            response_data = response.json()
            event_id = response_data.get("event_id")
            if not event_id:
                raise Exception("EVENT_ID not found in the response.")
            status_url = f"{API_ENDPOINT}/{event_id}"
            with session.get(status_url, stream=True, timeout=10, proxies=proxies) as stream_response:
                if stream_response.status_code != 200:
                    raise Exception(f"Streaming GET request failed with status {stream_response.status_code}: {stream_response.text}")
                for line in stream_response.iter_lines(decode_unicode=True, delimiter="\n\n"):
                    if line.startswith("event:"):
                        event_parts = line.split("\ndata: ")
                        if len(event_parts) < 2:
                            continue
                        event_type = event_parts[0].split(": ")[1].strip()
                        data = event_parts[1].strip()
                        if event_type == "error":
                            raise Exception(f"Error occurred: {data}")
                        elif event_type == "complete":
                            print(f"Received: {data}")
                            return
    except requests.Timeout:
        print("Request timed out.")
        return True
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return True
    except Exception as e:
        raise str(e)

def main():
    data = [access_key]
    print(make_request(data))

if __name__ == "__main__":
    main()
