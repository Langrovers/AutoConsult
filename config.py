import torch


class Config:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    whisper_model_type = "base"
    embedding_model = "speechbrain/spkrec-ecapa-voxceleb"


