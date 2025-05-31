import torch
import torch.nn as nn

class Wav2Lip(nn.Module):
    def __init__(self):
        super(Wav2Lip, self).__init__()
        # Minimal layers - replace with real model for actual use
        self.dummy_layer = nn.Linear(10, 10)
    
    def forward(self, face, audio):
        # Dummy forward - replace with real forward pass
        return face
