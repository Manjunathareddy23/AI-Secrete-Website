from gtts import gTTS
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('text', type=str)
parser.add_argument('--output_path', type=str, default="tmp.wav")
args = parser.parse_args()

tts = gTTS(args.text)
tts.save(args.output_path)
#clone
