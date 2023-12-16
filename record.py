import os
import threading
import wave
from datetime import datetime

import pyaudio

from transcriber import Transcriber


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.is_paused = False
        self.thread = None
        self.record_counter = 0
        self.path = os.path.join("records/user1", datetime.today().strftime(format="%d%m%y-%H%M%S"))
        self.transcriber = Transcriber()

    def start_or_resume_recording(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not self.is_recording:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                          frames_per_buffer=1024)
            self.is_recording = True
            self.is_paused = False
            self.thread = threading.Thread(target=self.record)
            self.thread.start()
            return "Recording started..."
        elif self.is_paused:
            self.is_paused = False
            return "Recording resumed..."
        else:
            return "Recording is already in progress"

    def record(self):
        while self.is_recording:
            if not self.is_paused:
                data = self.stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)

    def pause_recording(self):
        if self.is_recording and not self.is_paused:
            self.is_paused = True
            return "Recording paused"
        else:
            return "Recording is not in progress or already paused"

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.thread.join()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            filename = os.path.join(self.path, f"recording_{self.record_counter}.wav")
            sound_file = wave.open(filename, "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(self.frames))
            sound_file.close()

            self.record_counter += 1
            self.frames = []

            transcription_filename = os.path.join(self.path, f"transcription_{self.record_counter}.txt")
            self.transcriber.transcribe(
                filename,
                transcription_filename)

            return f"Recording stopped and saved as '{filename}'.\nTranscription: {transcription_filename}"
        else:
            return "Recording not started"

    def __del__(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
