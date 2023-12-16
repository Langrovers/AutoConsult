import glob
import json
import os
from string import Template
from time import sleep
from timeit import default_timer as timer

from neo4j import GraphDatabase

from config import Config
from gpt.graph import process_gpt
from prompts.cypher import *
from .cypher import generate_cypher


def neo4j_ingestion():
    """Executes Cypher statements from a file for data ingestion into a Neo4j graph database.

    Reads Cypher statements from a file and executes them against a Neo4j database instance.
    Logs any failed statements to a separate file.

    Uses:
        Config.NEO4J_URI: URL for the Neo4j database.
        Config.NEO4J_USERNAME: Username for the Neo4j database.
        Config.NEO4J_PASSWORD: Password for the Neo4j database.
        Config.graph_data_path: Path where the Cypher statements file is located.
    """
    gds = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD))

    with open(os.path.join(Config.graph_data_path, "cyphers.txt"), "r") as file:
        cypher_statements = file.readlines()
    for i, stmt in enumerate(cypher_statements):
        print(f"Executing cypher statement {i + 1} of {len(cypher_statements)}")
        sleep(0.5)
        try:
            gds.execute_query(stmt.strip())
        except Exception as e:
            with open(os.path.join(Config.graph_data_path, "failed_statements.txt"),
                      "a") as f:
                f.write(f"{stmt.strip()} - Exception: {e}\n")


def extract_entities_relationships(folder, prompt_template):
    """Extracts entities and relationships from text files in a folder using a given prompt template.

   Args:
       folder (str): Name of the folder containing text files.
       prompt_template (str): Template for generating prompts for the GPT model.

   Returns:
       list: A list of JSON objects representing the extracted entities and relationships.
   """
    start = timer()
    files = glob.glob(f"./data/{folder}/*")
    print(files)
    system_msg = "You are a helpful expert who extracts information from documents."
    print(f"Running pipeline for {len(files)} files in {folder} folder")
    results = []
    for i, file in enumerate(files):
        print(f"Extracting entities and relationships for {file}")
        try:
            with open(file, "r") as f:
                text = f.read().rstrip()
                print(text)
                prompt = Template(prompt_template).substitute(ctext=text)
                result = process_gpt(prompt, system_msg=system_msg)
                results.append(json.loads(result))
        except Exception as e:
            print(f"Error processing {file}: {e}")
    end = timer()
    print(f"Pipeline completed in {end - start} seconds")
    return results




def ingestion_pipeline():
    """Coordinates the ingestion pipeline for processing and ingesting data into Neo4j.

    The function performs the following steps:
    1. Extracts entities and relationships from specified folders using corresponding prompt templates.
    2. Generates Cypher statements for these entities and relationships.
    3. Executes the Cypher statements to ingest the data into a Neo4j graph database.
    """
    folders = {
        "customers": customer_prompt_template,
        "dealers": action_dealer_template,
    }

    # Extrating the entites and relationships from each fo  lder, append into one json_object
    entities_relationships = []
    for key, value in folders.items():
        entities_relationships.extend(extract_entities_relationships(key, value))

    # Generate and execute cypher statements
    generate_cypher(entities_relationships)
