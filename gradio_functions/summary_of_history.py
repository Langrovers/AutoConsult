import os
from config import Config
from gpt.summary_of_history import summary_pipeline


def get_summary_of_customer():
    """Compiles and summarizes customer interactions from text files in a specified directory.

      Reads all '.txt' files from subfolders in the user history path, concatenates their content, and then processes
      this combined content through a summary pipeline to generate a summary of customer interactions.

      Returns:
          The summarized content from the customer interaction files, as processed by the summary pipeline.
      """
    user_path = Config.user_history_path
    combined_content = ""
    for folder in os.listdir(user_path):
        for filename in os.listdir(os.path.join(user_path, folder)):
            if filename.endswith(".txt"):
                with open(os.path.join(user_path, folder, filename), 'r') as file:
                    combined_content += file.read() + "\n"

    return summary_pipeline(combined_content)
