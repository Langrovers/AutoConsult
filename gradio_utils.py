import gradio as gr

from record import AudioRecorder

audio_recorder = AudioRecorder()


def start_or_resume_recording():
    return audio_recorder.start_or_resume_recording()


def pause_recording():
    return audio_recorder.pause_recording()


def stop_recording():
    return audio_recorder.stop_recording()


with gr.Blocks() as app:
    gr.Markdown("### Audio Recorder")
    gr.Markdown(
        "Press 'Start/Resume Recording' to record or resume audio, 'Pause Recording' to pause, and 'Stop Recording' to end and save the audio.")
    start_resume_btn = gr.Button("Start/Resume Recording")
    pause_btn = gr.Button("Pause Recording")
    stop_btn = gr.Button("Stop Recording")
    status_label = gr.Label()

    start_resume_btn.click(fn=start_or_resume_recording, inputs=[], outputs=status_label)
    pause_btn.click(fn=pause_recording, inputs=[], outputs=status_label)
    stop_btn.click(fn=stop_recording, inputs=[], outputs=status_label)
