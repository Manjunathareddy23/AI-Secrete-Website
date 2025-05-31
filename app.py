import streamlit as st
import subprocess
import os


def run_wav2lip(face_path, audio_path, output_path):
    cmd = [
        "python", "./Wav2Lip/inference.py",
        "--checkpoint_path", "./checkpoints/wav2lip.pth",  # your trained checkpoint
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path,
    ]
    print("Running command:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    st.title("Wav2Lip Lip Sync Demo")
    
    face_file = st.file_uploader("Upload face video/image", type=["mp4", "jpg", "png"])
    audio_file = st.file_uploader("Upload audio", type=["wav", "mp3"])
    
    if face_file and audio_file:
        with open("input_face.mp4", "wb") as f:
            f.write(face_file.getbuffer())
        with open("input_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
            
        output_path = "result.mp4"
        if st.button("Generate Lip-Synced Video"):
            if run_wav2lip_inference("input_face.mp4", "input_audio.wav", output_path):
                st.video(output_path)

if __name__ == "__main__":
    main()
