from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def sales_assistant_pipeline(text):
    chat = ChatOpenAI(temperature=0)

    template = """Bir AI satış asistanı olarak görev yapmanı istiyorum.
    Bu rolde, telefon konuşmaları sırasında müşteri temsilcisi ile müşteri arasındaki diyalogu analiz etmek ve müşteri temsilcisine yardımcı olmak temel görevindir.
    Yanıtların, müşterinin ihtiyaçlarını anlamak, etkili çözümler önermek ve şirketin satış hedeflerine ulaşmasına yardımcı olacak tavsiyeler içermelidir.
    Aynı zamanda, müşteri memnuniyetini artıracak önerilerde bulunmalı ve her zaman profesyonel ve yardımsever bir tutum sergilemelisin.
    Müşteri temsilcisine yapacağın önerilerin kısa ve net olmalı. Örneğin:
    - Müşterinin ana sorunu:...
    - Müşteriyi daha iyi anlamak için şu soruyu sorabilirsiniz:...
    - Sorunu çözmek için şu adımları uygulayabilirsiniz:...
    
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)

    return chain.run(text=text)


def summary_pipeline(text):
    chat = ChatOpenAI(temperature=0)

    template = """Bir AI müşteri özet asistanı olarak görev yapmanı istiyorum.
    Bu rolde, müşteri ve müşteri temsilcisi arasındaki telefon görüşmelerini analiz etmek ve müşterinin geçmişteki aramalarındaki ana dertlerini madde madde çıkarmak temel görevindir.
    Yanıtların, müşterinin geçmiş aramalarındaki önemli konuları kısa ve net bir şekilde özetlemeli ve müşteri temsilcisine bu bilgilerle nasıl daha etkili yardımcı olabileceğine dair öneriler sunmalıdır.
    Örnek özetler:
    - Müşteri geçmişte kaza yapmış ve bununla ilgili destek istemiş.
    - Müşteri X marka araba satın almak istemiş ancak karar bağlanamamış.
    Her özetin ardından, müşteri temsilcisine müşteriyle daha verimli iletişim kurmasına yardımcı olacak öneriler vermelisin."""

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    memory = ConversationBufferMemory()
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)

    return chain.run(text=text)