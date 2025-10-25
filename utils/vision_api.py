# utils/vision_api.py

from google.cloud import vision
from google.oauth2 import service_account
import streamlit as st
import os

# Define the path to your NEW service key file (MUST MATCH app.py)
CREDENTIALS_PATH = r"D:\changed_project\iship_project\credentials\ai-style-curator-5c593f12304a.json"

def detect_objects(image_content):
    try:
        # 1. Explicitly load the credentials from the new file
        if not os.path.exists(CREDENTIALS_PATH):
            # This should have been caught in app.py, but is a good safeguard
            raise FileNotFoundError(f"Service account key not found at: {CREDENTIALS_PATH}")
            
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
        
        # 2. Initialize Vision API client with explicit credentials
        # This is the fix for the 401 error inside this specific function
        client = vision.ImageAnnotatorClient(credentials=credentials)
        image = vision.Image(content=image_content)

        # Detect localized objects in the image
        response = client.object_localization(image=image)
        objects = response.localized_object_annotations

        # Handle API errors gracefully
        if response.error.message:
            st.error(f"Vision API Error: {response.error.message}")
            return []

        return objects

    except Exception as e:
        st.error(f"An error occurred in detect_objects: {e}")
        return []