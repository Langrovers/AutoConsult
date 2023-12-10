import concurrent.futures
import contextlib
import datetime
import wave

import numpy as np
import torch
import whisper_timestamped as whisper
from pyannote.audio import Audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment
from sklearn.cluster import AgglomerativeClustering

from config import Config
from utils import suppress_stdout


class WhisperTranscriber:
    def __init__(self, model=Config.whisper_model_type, device=Config.device):
        self.model = whisper.load_model(model, device=device)

    def transcribe(self, filename):
        with suppress_stdout():
            result = self.model.transcribe(filename, language="Turkish", verbose=False)
        return result["text"], result["segments"]


class Transcriber:

    def __init__(self, model_path=Config.embedding_model):
        self.model = WhisperTranscriber()
        self.embedding_model = PretrainedSpeakerEmbedding(model_path, device=torch.device(Config.device))
        self.audio = Audio()

    def segment_embedding(self, segment, path):
        start = segment["start"]
        with contextlib.closing(wave.open(path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        end = min(duration, segment["end"])
        clip = Segment(start, end)
        waveform, sample_rate = self.audio.crop(path, clip)
        return self.embedding_model(waveform[None])

    def calculate_embeddings(self, segments, path):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_embeddings = {executor.submit(self.segment_embedding, segment, path): segment for segment in
                                 segments}
            for future in concurrent.futures.as_completed(future_embeddings):
                segment = future_embeddings[future]
                try:
                    embedding = future.result()
                    yield embedding
                except Exception as exc:
                    print('%r generated an exception: %s' % (segment, exc))

    def transcribe(self, audio_path, output_path):
        result, segments = self.model.transcribe(audio_path)
        with contextlib.closing(wave.open(audio_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        embeddings = np.zeros(shape=(len(segments), self.segment_embedding(segments[0], audio_path).shape[1]))

        for i, embedding in enumerate(self.calculate_embeddings(segments, audio_path)):
            embeddings[i] = embedding

        embeddings = np.nan_to_num(embeddings)

        clustering = AgglomerativeClustering(2).fit(embeddings)
        labels = clustering.labels_
        for i in range(len(segments)):
            segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

        with open(output_path, "w") as f:
            for (i, segment) in enumerate(segments):
                if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                    f.write("\n" + segment["speaker"] + ' ' + str(self.time(segment["start"])) + '\n')
                f.write(segment["text"][1:] + ' ')

    def time(self, secs):
        return datetime.timedelta(seconds=round(secs))
