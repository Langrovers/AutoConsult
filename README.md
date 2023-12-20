# README.md

# AutoConsult

## Overview
This project was conducted during the Generative AI hackathon organized by Borusan Otomotiv. The aim of the project is to create an AI-supported customer call center.

Calls made by customers have been converted to text using Whisper. Additionally, diarization has been used to distinguish between speakers in the conversation. Metadata related to the customer and conversations with customer representatives have been recorded in a graph database in Neo4j using LLM.

Functions of the project:
- The customer representative can record during the call and convert this recording into text.
- At the beginning of the call, the customer representative can learn a summary of the customer's previous calls.
- During the current call, to provide better service to the customer, the representative can receive live advice from the language model.
- The representative can speak live with the company data stored in the Graph Database and quickly answer potential questions of the customer.

## Structure
- `call_to_text/`: Modules for transcribing calls.
  - `record.py`: Handles audio recording.
  - `transcriber.py`: Transcribes audio to text.
- `data/`: Data storage.
  - `call_data/`: Stores call records.
  - `graph_data/`: Stores graph data and cypher text.
- `gpt/`: Natural Language Processing.
  - `graph.py`: Creates graph from text.
  - `sales_assistant.py`: During the current call, the customer representative can receive instant advice.
  - `summary_of_history.py`: Brings a summary of the customer's previous calls.
- `gradio_functions/`: Gradio app components.
  - `audio_record.py`: Records audio through the interface.
  - `sales_assistant.py`: Provides sales assistance.
- `graph/`: Graph generation logic.
  - `cypher.py`: Cypher queries for graph databases.
  - `ingestion.py`: Ingests data into the graph database.
- `prompts/`: Prompts for GPT models.
- `main.py`: Entry point for the application.
- `config.py`: Configuration settings.
- `poetry.lock`: Poetry dependencies lock file.

## Installation
1. Clone the repository.
2. Install poetry. https://python-poetry.org/
3. Install dependencies using Poetry. ***poetry install***


## Usage
1. Add your required API keys in the `config.py` file.
2. Change data paths `config.py`
3. Run `main.py` to start the application.

## Authors
- Oğuzhan Kır https://github.com/oguzhankir
- Gökay Aydoğan https://github.com/gokayfem

## Acknowledgments
Thanks to all contributors.
