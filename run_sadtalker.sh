#!/bin/bash

# Parameters: $1=image_path, $2=text, $3=output_path
IMG_PATH=$1
TEXT=$2
OUTPUT_PATH=$3

cd SadTalker

# Convert text to audio using gTTS
python3 scripts/tts_gtts.py "$TEXT" --output_path "../tmp.wav"

# Run SadTalker
python3 inference.py \
  --driven_audio ../tmp.wav \
  --source_image "../$IMG_PATH" \
  --result_dir "../$OUTPUT_PATH" \
  --enhancer gfpgan \
  --preprocess full \
  --still

cd ..
chmod +x run_sadtalker.sh
