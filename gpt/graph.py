from time import sleep
from config import Config
import openai
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import Neo4jGraph
from langchain.prompts.prompt import PromptTemplate
from prompts.cyper import *

def process_gpt(file_prompt, system_msg):
    """Uses GPT-4 to generate a response based on a file prompt and system message.

        Args:
            file_prompt (str): The user's prompt from a file.
            system_msg (str): A system message to provide context for the GPT model.

        Returns:
            str: The response generated by GPT-4.
        """
    completion = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        max_tokens=4096,
        temperature=0,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": file_prompt},
        ],
    )
    nlp_results = completion.choices[0].message.content
    sleep(8)
    return nlp_results

def talk_graph(user_input):
    """Processes user input using a graph-based QA system with GPT-4.

    Args:
        user_input (str): The user's input question or statement.

    Returns:
        str: The result from the graph-based QA system.
    """
    llm = ChatOpenAI(openai_api_key=Config.openai_api_key, temperature=0, model_name="gpt-4-1106-preview")

    cypher_prompt = PromptTemplate(
        template=cypher_generation_template,
        input_variables=["schema", "question"]
    )

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
    )

    graph = Neo4jGraph(url=Config.NEO4J_URI, username=Config.NEO4J_USERNAME, password=Config.NEO4J_PASSWORD)
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt
    )
    result = chain(user_input)

    #TODO: GENERATE REPORT FROM RESULT
    return str(result)

