import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
def prep_image(image_path):
    """Uploads the image file to Gemini and returns the uploaded file object."""
    sample_file = genai.upload_file(path=image_path, display_name="SketchOCR")
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    return sample_file

def extract_text_from_image(sample_file, prompt):
    """Extracts text from image using Gemini with the given prompt."""
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    response = model.generate_content([sample_file, prompt])
    return response.text