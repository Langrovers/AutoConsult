import gradio as gr
import os
from record import AudioRecorder
from gpt import sales_assistant_pipeline, summary_pipeline

audio_recorder = AudioRecorder()


def start_or_resume_recording():
    return audio_recorder.start_or_resume_recording()


def pause_recording():
    return audio_recorder.pause_recording()


def stop_recording():
    return audio_recorder.stop_recording()


def get_advice_from_gpt():
    combined_content = ""
    for filename in os.listdir("/home/oguz/Desktop/personal/speech-graph-generator/records/user1/131223-202906"):
        if filename.endswith(".txt"):
            with open(os.path.join("/home/oguz/Desktop/personal/speech-graph-generator/records/user1/131223-202906",
                                   filename), 'r') as file:
                combined_content += file.read() + "\n"

    return sales_assistant_pipeline(combined_content)

def get_summary_of_customer():
    user_path = "/home/oguz/Desktop/personal/speech-graph-generator/records/user1"
    combined_content = ""
    for folder in os.listdir(user_path):
        for filename in os.listdir(os.path.join(user_path,folder)):
            if filename.endswith(".txt"):
                with open(os.path.join(user_path, folder, filename), 'r') as file:
                    combined_content += file.read() + "\n"

    return summary_pipeline(combined_content)

def talk_graph(input_text):
    return input_text


with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("### Audio Recorder")
    gr.Markdown(
        "Press 'Start/Resume Recording' to record or resume audio, 'Pause Recording' to pause, and 'Stop Recording' to end and save the audio.")
    start_resume_btn = gr.Button("Start/Resume Recording")
    pause_btn = gr.Button("Pause Recording")
    stop_btn = gr.Button("Stop Recording")
    get_advice_btn = gr.Button("Get Advice From GPT")
    get_summary_btn = gr.Button("Get Summary of Customer")


    talk_graph_btn = gr.Button("Talk graph")
    input_text = gr.Textbox(placeholder="Enter text here", label="Input Text")

    status_label = gr.Label()

    start_resume_btn.click(fn=start_or_resume_recording, inputs=[], outputs=status_label)
    pause_btn.click(fn=pause_recording, inputs=[], outputs=status_label)
    stop_btn.click(fn=stop_recording, inputs=[], outputs=status_label)
    get_advice_btn.click(fn=get_advice_from_gpt, inputs=[], outputs=status_label)
    get_summary_btn.click(fn=get_summary_of_customer, inputs=[], outputs=status_label)

    talk_graph_btn.click(fn=talk_graph, inputs=[input_text], outputs=status_label)
