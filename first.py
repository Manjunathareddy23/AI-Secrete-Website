import streamlit as st
import requests
import base64
import time
import os
from gtts import gTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DID_API_KEY = os.getenv("DID_API_KEY")

st.set_page_config(page_title="AI Talking Avatar", layout="centered")

# === Tailwind CSS Injection ===
tailwind_css = """
<style>
@import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');

body {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
.glass-box {
    backdrop-filter: blur(15px);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: transform 0.3s ease;
}
.glass-box:hover {
    transform: scale(1.01);
}
.animated-container {
    animation: float 6s ease-in-out infinite;
}
@keyframes float {
    0% { transform: translatey(0px); }
    50% { transform: translatey(-15px); }
    100% { transform: translatey(0px); }
}
.download-btn {
    background-color: #0ea5e9;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 9999px;
    font-weight: bold;
    text-decoration: none;
}
.download-btn:hover {
    background-color: #0284c7;
}
</style>
"""
st.markdown(tailwind_css, unsafe_allow_html=True)

# === Sidebar ===
with st.sidebar:
    st.header("🔧 Configuration")
    language = st.selectbox("🔤 TTS Language", ["en", "hi", "te", "ta", "ml", "bn", "gu", "kn", "mr", "ur"], index=0)

# === Title ===
st.markdown("<div class='text-4xl font-bold text-center mb-4'>🎙️ AI Talking Avatar Generator</div>", unsafe_allow_html=True)
st.markdown("<p class='text-center mb-6'>Upload a photo, enter text, and generate a lifelike speaking avatar using gTTS + D-ID APIs.</p>", unsafe_allow_html=True)

# === Upload UI with glassmorphism ===
with st.container():
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("📷 Upload a Face Image (.jpg/.jpeg/.png)", type=["jpg", "jpeg", "png"])
    input_text = st.text_area("📝 Enter the text you want the avatar to say")
    generate_btn = st.button("🚀 Generate Talking Avatar")
    st.markdown("</div>", unsafe_allow_html=True)

if generate_btn:
    if not uploaded_image or not input_text:
        st.warning("Please upload an image and enter some text.")
    elif not DID_API_KEY:
        st.error("❌ D-ID API key not found. Please add it to the .env file.")
        st.stop()
    else:
        # === gTTS Audio Generation ===
        with st.spinner("🎧 Generating audio using gTTS..."):
            try:
                tts = gTTS(text=input_text, lang=language)
                audio_path = "output_audio.mp3"
                tts.save(audio_path)
            except Exception as e:
                st.error(f"❌ gTTS failed to generate audio: {str(e)}")
                st.stop()

        # === D-ID Video Generation ===
        with st.spinner("📡 Uploading to D-ID and generating video..."):
            image_data = uploaded_image.read()
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            with open(audio_path, "rb") as audio_file:
                audio_b64 = base64.b64encode(audio_file.read()).decode("utf-8")

            did_url = "https://api.d-id.com/talks"
            headers = {
                "Authorization": f"Basic {DID_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "script": {
                    "type": "audio",
                    "audio": audio_b64
                },
                "source": {
                    "type": "image",
                    "image": image_b64
                },
                "config": {
                    "fluent": True,
                    "pad_audio": 0.2
                }
            }

            response = requests.post(did_url, headers=headers, json=payload)
            if response.status_code != 200:
                st.error("❌ D-ID API failed.")
                st.stop()

            talk_id = response.json()["id"]

            # Poll for video result
            for _ in range(20):
                status_res = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
                result = status_res.json()
                if result.get("result_url"):
                    video_url = result["result_url"]
                    break
                time.sleep(2)
            else:
                st.error("❌ Timed out waiting for video.")
                st.stop()

            video_data = requests.get(video_url).content
            video_path = "talking_avatar.mp4"
            with open(video_path, "wb") as f:
                f.write(video_data)

        # === Display Video with Animation ===
        st.markdown("<div class='glass-box animated-container text-center'>", unsafe_allow_html=True)
        st.video(video_path)
        st.markdown("<p class='mt-4 text-xl text-green-300 font-semibold'>✅ Video Successfully Generated!</p>", unsafe_allow_html=True)

        # === Download Button ===
        with open(video_path, "rb") as f:
            video_bytes = f.read()
            b64 = base64.b64encode(video_bytes).decode()
            download_link = f'<a class="download-btn mt-4 inline-block" href="data:video/mp4;base64,{b64}" download="talking_avatar.mp4">📥 Download Video</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
