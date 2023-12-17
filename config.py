import os

import pandas as pd
import torch


class Config:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    whisper_model_type = "large"
    embedding_model = "speechbrain/spkrec-ecapa-voxceleb"
    openai_api_key = "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"
    user_history_path = "/home/oguz/Desktop/personal/AutoConsult/data/call_data/records/user1"
    sales_asistant_dialog_path = os.path.join(user_history_path,
                                              sorted([pd.to_datetime(f) for f in os.listdir(user_history_path)])[
                                                  -1].strftime(
                                                  format="%d%m%y-%H%M%S"))
    graph_data_path = "/home/oguz/Desktop/personal/AutoConsult/data/graph_data"
    NEO4J_URI = "neo4j+s://725f44d4.databases.neo4j.io"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "NtCli2aXlH3YgnTERiEPG92baITF9ZbArkki1o1e0XM"
    AURA_INSTANCEID = "725f44d4"
    AURA_INSTANCENAME = "Instance01"
    GENERATE_CYPER = False
    INGEST_NEO4J = False
