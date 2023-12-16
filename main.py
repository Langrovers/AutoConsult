import gradio as gr

from gpt.graph import talk_graph
from gradio_functions.audio_record import *
from gradio_functions.sales_asistant import *
from gradio_functions.summary_of_history import *
from graph.ingestion import ingestion_pipeline, neo4j_ingestion

os.environ["OPENAI_API_KEY"] = Config.openai_api_key

with gr.Blocks(theme=gr.themes.Soft()) as app:
    start_resume_btn = gr.Button("Start/Resume Recording")
    stop_btn = gr.Button("Stop Recording")
    get_advice_btn = gr.Button("Get Advice From GPT")
    get_summary_btn = gr.Button("Get Summary of Customer")

    status_label = gr.Label()

    start_resume_btn.click(fn=start_or_resume_recording, inputs=[], outputs=status_label)
    stop_btn.click(fn=stop_recording, inputs=[], outputs=status_label)
    get_advice_btn.click(fn=ask_sales_asistant, inputs=[], outputs=status_label)
    get_summary_btn.click(fn=get_summary_of_customer, inputs=[], outputs=status_label)

    chatbot = gr.ChatInterface(fn=talk_graph, examples=["Which dealers provide service for BMW vehicles?",
                                                        "Find all vehicles owned by customers over 40 years old."],
                               title="Sales Assistant Bot")

if __name__ == "__main__":
    if Config.GENERATE_CYPER:
        ingestion_pipeline()

    if Config.INGEST_NEO4J:
        neo4j_ingestion()

    app.launch()
