import streamlit as st
import subprocess
import os

st.title("SadTalker Video Generator")

uploaded_image = st.file_uploader("Upload face image", type=["jpg", "png"])
input_text = st.text_area("Enter text")

if st.button("Generate Talking Video") and uploaded_image and input_text:
    image_path = "input.jpg"
    output_path = "output"

    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    cmd = ["bash", "run_sadtalker.sh", image_path, input_text, output_path]
    subprocess.run(cmd)

    result_video = os.path.join(output_path, "input_000.mp4")
    if os.path.exists(result_video):
        st.success("Video generated!")
        st.video(result_video)
    else:
        st.error("Video generation failed.")
