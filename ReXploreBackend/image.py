import base64
import io
import os
import re
import requests
import dotenv
from PIL import Image
import pollinations as ai

dotenv.load_dotenv()

def extract_summary(text):
    text = text.replace("#", "").strip().lower()
    match = re.search(r"summary(.*?)highlights", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def fix_base64_padding(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return data

def generate_image(title, summary):
    try:
        extracted_summary = extract_summary(summary)
        prompt = f"{title.strip()}: {extracted_summary.strip()}"
        model_obj = ai.ImageModel(
            model=ai.flux_pro,
            width=1280,
            height=720,
            seed=2342342340,
            enhance=True,
            nologo=True
        )
        image = model_obj.generate(
            prompt=prompt,
            negative="low quality, blurry, pixelated",
            save=True,
            file="image.png"
        )
        if type(image) == str:
            print(f"An error occurred during image generation: {image}")
            return None
        image_url = image.params.get("url")
        if image_url:
            img_data = requests.get(image_url).content
            base64_encoded = base64.b64encode(img_data).decode("utf-8")
            return f"data:image/png;base64,{base64_encoded}"
        return None
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return None

def verify_image(image_data):
    try:
        image_stream = io.BytesIO(image_data)
        img = Image.open(image_stream)
        img.verify()
        return True
    except Exception as e:
        print(f"Error verifying image: {e}")
        return False

def upload_image(data_uri, api_key):
    image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    try:
        base64_image = fix_base64_padding(data_uri.split(",")[1])
        url = f"https://api.imgbb.com/1/upload?key={api_key}"
        response = requests.post(url, data={"image": base64_image}).json()
        if response.get("status") == 200:
            image_url = response["data"]["display_url"]
        else:
            print(f"Error uploading image: {response}")
            image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    except Exception as e:
        print(f"Error uploading image: {e}")
        image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    finally:
        return image_url

def fetch_image(title, summary, api_key):
    image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    try:
        data_uri = generate_image(title, summary)
        if data_uri:
            base64_image = fix_base64_padding(data_uri.split(",")[1])
            image_data = base64.b64decode(base64_image)
            if verify_image(image_data):
                image_url = upload_image(data_uri, api_key)
        else:
            image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    except Exception as e:
        print(f"Error fetching image: {e}")
        image_url = "https://i.ibb.co/qdC1nSx/landscape-placeholder-e1608289113759.png"
    finally:
        os.remove("image.png")
        return image_url