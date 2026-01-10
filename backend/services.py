import os
import json
import base64
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Keys
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🛠️ Configuration for Gemini
# Using gemini-2.5-flash (faster, cheaper, still very capable)
# Alternative: "models/gemini-2.5-pro" for maximum capability (slower, more expensive)
MODEL_NAME = "models/gemini-2.5-flash"
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
)

def get_image_bytes(image_url):
    """Downloads an image and returns its raw bytes."""
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    raise Exception(f"Failed to download image from {image_url}")

def audit_room(image_url):
    """Performs a spatial audit of a room for accessibility."""
    try:
        image_data = get_image_bytes(image_url)
        img = Image.open(BytesIO(image_data))

        prompt = """You are an expert Accessibility Architect (AODA compliant). Analyze this real estate photo.
Identify the single most critical accessibility barrier (e.g., stairs, narrow doorway, high tub).
Return a strict JSON object with these keys:
- barrier_detected: string (The issue found)
- renovation_suggestion: string (The fix, e.g., 'Install vertical platform lift')
- estimated_cost_usd: integer (Rough estimate)
- compliance_note: string (Reference standard codes like '1:12 slope ratio')
- mask_prompt: string (A visual description of the specific area to mask/erase for inpainting, e.g., 'the concrete stairs leading to the porch')
- image_gen_prompt: string (A prompt for the image generator to fill in the masked area, e.g., 'A modern wooden ramp with aluminum railings, photorealistic, 8k, cinematic lighting, keeping original siding style')"""

        response = model.generate_content([prompt, img])
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from Gemini: {str(e)}")
    except Exception as e:
        raise Exception(f"Audit failed: {str(e)}")

def generate_renovation(image_url, prompt, mask_prompt):
    """Uses Stability AI's Search-and-Replace to visualize the change."""
    image_data = get_image_bytes(image_url)
    
    # Stability AI V2 Search and Replace Endpoint
    url = "https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"
    
    headers = {
        "authorization": f"Bearer {os.getenv('STABILITY_KEY')}",
        "accept": "image/*" # We want the raw image back
    }
    
    files = {
        "image": ("image.webp", image_data, "image/webp")
    }
    
    data = {
        "prompt": prompt,
        "search_prompt": mask_prompt,
        "output_format": "webp",
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.content
    else:
        # If visual gen fails, we still want the audit, so we log the error
        print(f"Stability AI Error: {response.json()}")
        return None