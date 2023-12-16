from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from prompts.summary_of_history import SUMMARY_OF_HISTORY_PROMPT


def summary_pipeline(text):
    """Executes a summary generation pipeline for a given text using a language model.

    Args:
        text (str): The input text to be summarized.

    Returns:
        The output from the language model chain, providing a summary of the input text.
    """
    chat = ChatOpenAI(temperature=0)

    template = SUMMARY_OF_HISTORY_PROMPT

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)

    return chain.run(text=text)
