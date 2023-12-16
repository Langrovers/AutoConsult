import torch


class Config:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    whisper_model_type = "large"
    embedding_model = "speechbrain/spkrec-ecapa-voxceleb"
    openai_api_key = ""


