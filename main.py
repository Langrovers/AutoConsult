from config import Config
from gradio_utils import *

os.environ["OPENAI_API_KEY"] = Config.openai_api_key
if __name__ == "__main__":
    app.launch()
