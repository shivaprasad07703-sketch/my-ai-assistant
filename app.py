import streamlit as st
import requests
import io
from PIL import Image

# --- Configuration ---
# Replace 'YOUR_HUGGINGFACE_API_TOKEN' with your actual free token from Hugging Face
HF_TOKEN = st.secrets["HF_TOKEN"]
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Free Open-Source Models on Hugging Face
#/runwayml/stable-diffusion-v1-5
TEXT_MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
IMAGE_MODEL_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"



# --- UI Setup ---
st.set_page_config(page_title="My AI Assistant", layout="centered")
st.title("🤖 My Custom AI Assistant")
st.write("Generate text conversations and images using free open-source AI models.")

st.divider()

# --- Feature 1: Text Generation (Chat) ---
st.header("💬 Chat Assistant")
user_text = st.text_area("Ask me a question or give me a prompt:")

if st.button("Generate Text"):
    if user_text:
        with st.spinner("Thinking..."):
            payload = {"inputs": user_text, "parameters": {"max_new_tokens": 250}}
            response = requests.post(TEXT_MODEL_URL, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                # Extract and format the generated text
                generated_text = response.json()[0]['generated_text']
                st.success("Response:")
                st.write(generated_text)
            else:
                st.error("Failed to connect to the text AI. It might be loading, try again in a minute.")
    else:
        st.warning("Please enter some text first.")

st.divider()

# --- Feature 2: Image Generation ---
st.header("🎨 Image Generator")
image_prompt = st.text_input("Describe the image you want to create:")

if st.button("Generate Image"):
    if image_prompt:
        with st.spinner("Painting your image..."):
            payload = {"inputs": image_prompt}
            response = requests.post(IMAGE_MODEL_URL, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                # Convert the raw byte response into an image
                image = Image.open(io.BytesIO(response.content))
                st.image(image, caption=f"Prompt: {image_prompt}", use_column_width=True)
            else:
                st.error(f"Hugging Face Error: {response.text}")                
    else:
        st.warning("Please enter an image description first.")

st.divider()
st.caption("Note: Video generation requires heavy computing power and is usually implemented via paid APIs (like Replicate) or local high-end GPUs.")

# --- Feature 3: Video Generation ---
st.divider()
st.header("🎬 Video Generator")
st.write("Generate short video clips. (Note: Free video servers take 1-3 minutes to load!)")

video_prompt = st.text_input("Describe the video scene you want to create:")

if st.button("Generate Video"):
    if video_prompt:
        with st.spinner("Directing your scene... (This might take a few minutes)"):
            # Using a free open-source video model
            VIDEO_MODEL_URL = "https://router.huggingface.co/hf-inference/models/damo-vilab/text-to-video-ms-1.7b"
            payload = {"inputs": video_prompt}
            
            try:
                response = requests.post(VIDEO_MODEL_URL, headers=HEADERS, json=payload)
                
                if response.status_code == 200:
                    # Streamlit can play the video bytes directly!
                    st.video(response.content)
                    st.success("Scene generated successfully!")
                else:
                    # If the server is busy, it will tell us why here
                    st.error(f"Hugging Face Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.warning("Please enter a scene description first.")
