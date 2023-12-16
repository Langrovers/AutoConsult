import os

from config import Config
from gpt.sales_asistant import sales_assistant_pipeline


def ask_sales_asistant():
    """Aggregates content from text files in a directory and processes it through the sales assistant pipeline.

    Gathers the content of all '.txt' files in the specified sales assistant dialog path, combines them, and then
    runs the combined content through the sales assistant pipeline for processing.

    Returns:
        The output from the sales assistant pipeline after processing the aggregated content.
    """
    combined_content = ""
    for filename in os.listdir(Config.sales_asistant_dialog_path):
        if filename.endswith(".txt"):
            with open(os.path.join(Config.sales_asistant_dialog_path,
                                   filename), 'r') as file:
                combined_content += file.read() + "\n"

    return sales_assistant_pipeline(combined_content)
