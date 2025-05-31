import streamlit as st
from gtts import gTTS
import os
import subprocess
import tempfile
import base64

# Configure Streamlit page
st.set_page_config(page_title="AI Talking Avatar (Local Wav2Lip)", layout="centered")

# Tailwind CSS injection (optional for style)
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

# Sidebar language selection
with st.sidebar:
    st.header("🔧 Configuration")
    language = st.selectbox("🔤 TTS Language", ["en", "hi", "te", "ta", "ml", "bn", "gu", "kn", "mr", "ur"], index=0)

# Title and instructions
st.markdown("<div class='text-4xl font-bold text-center mb-4'>🎙️ AI Talking Avatar Generator (Local)</div>", unsafe_allow_html=True)
st.markdown("<p class='text-center mb-6'>Upload a face image, enter text, and generate a talking avatar video locally using gTTS + Wav2Lip.</p>", unsafe_allow_html=True)

# Upload image and enter text
with st.container():
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("📷 Upload a Face Image (.jpg/.jpeg/.png)", type=["jpg", "jpeg", "png"])
    input_text = st.text_area("📝 Enter the text for the avatar to say")
    generate_btn = st.button("🚀 Generate Talking Avatar")
    st.markdown("</div>", unsafe_allow_html=True)

def save_temp_file(uploaded_file, suffix):
    """Save uploaded file temporarily."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

def run_wav2lip_inference(face_path, audio_path, output_path, checkpoint_path="checkpoints/wav2lip.pth"):
    """Run Wav2Lip inference using subprocess call."""
    cmd = [
        "python", "inference.py",
        "--checkpoint_path", checkpoint_path,
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Wav2Lip inference failed:\n{result.stderr}")

if generate_btn:
    if not uploaded_image or not input_text.strip():
        st.warning("Please upload an image and enter some text.")
    else:
        with st.spinner("🎧 Generating speech audio..."):
            try:
                # Save audio file temporarily
                tts = gTTS(text=input_text, lang=language)
                audio_temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                tts.save(audio_temp_path)
            except Exception as e:
                st.error(f"Error generating audio: {e}")
                st.stop()

        with st.spinner("🧠 Running Wav2Lip inference..."):
            try:
                # Save uploaded image temporarily
                face_temp_path = save_temp_file(uploaded_image, suffix=".png")

                # Output video path (temporary)
                output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

                # Run Wav2Lip inference locally
                run_wav2lip_inference(face_temp_path, audio_temp_path, output_video_path)

            except Exception as e:
                st.error(str(e))
                st.stop()

        # Display video
        st.markdown("<div class='glass-box animated-container text-center'>", unsafe_allow_html=True)
        st.video(output_video_path)
        st.markdown("<p class='mt-4 text-xl text-green-300 font-semibold'>✅ Video successfully generated!</p>", unsafe_allow_html=True)

        # Provide download link
        with open(output_video_path, "rb") as f:
            video_bytes = f.read()
            b64 = base64.b64encode(video_bytes).decode()
            download_link = f'<a class="download-btn mt-4 inline-block" href="data:video/mp4;base64,{b64}" download="talking_avatar.mp4">📥 Download Video</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
