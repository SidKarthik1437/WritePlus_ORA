import config
import os
os.environ['OPENAI_API_KEY'] = config.openAI

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

llm = OpenAI(temperature=1)

chat = ChatOpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

def Summarizer(body):
    texts = text_splitter.split_text(body)

    

    docs = [Document(page_content=t) for t in texts[:3]]

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    op = chain.run(docs)

    return(op)

def ChatSummarizer(body):
    template="You are a helpful assistant that summarizes {text}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    ai_message_prompt = AIMessagePromptTemplate.format()
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    return chat(chat_prompt.format_prompt(text=text).to_messages())


text = """
                     By India Today News Desk: As the cyclonic storm Biparjoy, which intensified into a very severe cyclonic storm, is approaching the coastline, heavy rains laced with gale winds are expected along the Karnataka coast and Bengaluru on Thursday, the India Meteorological Department (IMD) said.

The Met Department also said the monsoon is likely to reach Kerala on Friday.

While the gale winds will be witnessed at the center of the cyclone, the Konkan coast comprising Kerala, Karnataka and Goa will receive squally weather till June 12, said the IMD in its Wednesday bulletin.

Meanwhile, the Karnataka government and the district administration have stepped up measures to face the cyclonic impact for the next five days, reported The Hindu. The NDRF and SDRF teams have been alerted.

WIDESPREAD RAINS LIKELY IN KERALA
The IMD on Wednesday said that Kerala is likely to receive widespread rains across the state for five days. According to the weather agency, a mild monsoon onset over Kerala has been predicted as cyclone ‘Biprajoy’, which intensified into a very severe cyclonic storm on Wednesday.

A rain alert has been issued for Ernakulam district on Thursday as the region is expected to receive heavy rains.

Besides, widespread rains are expected in Thiruvananthapuram and Kollam districts on Friday (June 9).

Fishermen were not to venture into cyclone-hit areas in the Arabian Sea.

Kerala has recorded widespread rainfall activity across different stations. This is rainfall data from 8.30 am on Wednesday morning till 10 pm. Although, IMD hasn't officially announced the arrival of the Monsoon yet. IMD said that Kerala might witness Monsoon onset in next 48 hours.

HEATWAVE IN TAMIL NADU
Meanwhile, the Regional Meteorological Centre (RMC) in Chennai has issued a heatwave warning for some pockets in Tamil Nadu, Puducherry and Karaikal due to the cyclone intensifying.

The mercury is expected to rise up to 40 degrees Celsius in these regions.

On Wednesday, the highest temperature recorded in the state was 40.1 degrees Celsius in Tiruttani, followed by Karur – 40 degrees Celsius.

The weather department also predicted rain and thunderstorm activity in Ariyalur, Cuddalore, Thanjavur, Thiruvarur, Namakkal, Pudukottai and a few other regions on Thursday and Friday. Also, Chennai is to receive light shows for the next two days.


                     """

print(ChatSummarizer(text))