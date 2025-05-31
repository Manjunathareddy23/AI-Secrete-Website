import streamlit as st
import subprocess
import os

def run_wav2lip_inference(face_path, audio_path, output_path, checkpoint_path="./checkpoints/wav2lip.pth"):
    inference_py_path = "./Wav2Lip/inference.py"
    
    cmd = [
        "python", inference_py_path,
        "--checkpoint_path", checkpoint_path,
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path
    ]
    
    st.write("Running command:", " ".join(cmd))  # Debug print
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        st.error(f"Wav2Lip inference failed:\n{result.stderr}")
        raise RuntimeError("Wav2Lip inference failed")
    else:
        st.success("Wav2Lip inference completed successfully!")
    return output_path

# Streamlit UI
st.title("AI Secrete Website - Wav2Lip Video Generation")

st.write("Current working directory:", os.getcwd())

face_img = st.file_uploader("Upload face image (jpg/png)", type=["jpg", "png"])
audio_file = st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"])

if st.button("Generate Video") and face_img and audio_file:
    # Save uploaded files to temp paths
    face_path = "./temp_face.jpg"
    audio_path = "./temp_audio.wav"
    output_path = "./output/result.mp4"
    
    with open(face_path, "wb") as f:
        f.write(face_img.getbuffer())
    with open(audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
    
    try:
        video_path = run_wav2lip_inference(face_path, audio_path, output_path)
        st.video(video_path)
        st.success("Video generated successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
