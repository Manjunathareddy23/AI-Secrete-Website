import gradio as gr
import subprocess
import os

def generate_video(image, text):
    # Save uploaded image
    image_path = "input.jpg"
    output_path = "output"
    with open(image_path, "wb") as f:
        f.write(image.read())

    # Run shell script
    cmd = ["bash", "run_sadtalker.sh", image_path, text, output_path]
    subprocess.run(cmd)

    result_video = os.path.join(output_path, "input_000.mp4")
    if os.path.exists(result_video):
        return result_video
    else:
        return "Video generation failed or not found."

interface = gr.Interface(
    fn=generate_video,
    inputs=[
        gr.Image(type="file", label="Upload Face Image"),
        gr.Textbox(lines=2, label="Enter Text to Speak")
    ],
    outputs=gr.Video(label="Generated Talking Video"),
    title="SadTalker: Talking Face Generator",
    description="Upload a face image and input text to generate a lip-synced talking video."
)

if __name__ == "__main__":
    interface.launch()
