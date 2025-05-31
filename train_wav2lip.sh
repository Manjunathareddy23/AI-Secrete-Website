#!/bin/bash

# Step 1: Clone repo if not exists
if [ ! -d "Wav2Lip" ]; then
  git clone https://github.com/Rudrabha/Wav2Lip.git
fi

cd Wav2Lip

# Step 2: Create & activate virtual env (Linux/Mac)
if [ ! -d "env" ]; then
  python3 -m venv env
fi

# Activate virtualenv for this script run
source env/bin/activate

# Step 3: Install requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install tensorflow==1.15.0 torch torchvision

# Step 4: Download pretrained model if not exists
mkdir -p checkpoints
if [ ! -f "checkpoints/wav2lip.pth" ]; then
  wget https://storage.googleapis.com/df-wav2lip/models/wav2lip.pth -P checkpoints/
fi

# Step 5: Train model (replace paths as needed)
python train.py --data_root ./data/train --checkpoint_dir ./checkpoints --syncnet_wt 0

# Deactivate virtual environment
deactivate
