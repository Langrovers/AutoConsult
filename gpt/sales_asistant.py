from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from prompts.sales_asistant import SALES_ASISTANT_PROMPT


def sales_assistant_pipeline(text):
    """Processes text input through a sales assistant pipeline using a language model.

    Args:
        text (str): The text input provided by a user.

    Returns:
        The result from running the language model chain with the given text.
    """
    chat = ChatOpenAI(temperature=0)

    template = SALES_ASISTANT_PROMPT

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)

    return chain.run(text=text)
