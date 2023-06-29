import config
import os
import json
import streamlit as st
os.environ['OPENAI_API_KEY'] = config.openAI
import openai
import re
from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

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

def extract_numbers(string):
    pattern = r'-?\d+\.\d+'
    matches = re.findall(pattern, string)
    return matches


def Summarizer(body):
    texts = text_splitter.split_text(body)

    docs = [Document(page_content=t) for t in texts[:3]]

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    try:
        op = chain.run(docs)
    except Exception as e:
        print("Cannot summarize data: ", e)
        
        return body 
        

    return(op)

def ChatSummarizer(body):
    
    print("Analyzing News...")
    
    template="""You are a helpful assistant that summarizes text and gives the sentiment polarity in the scale -1 to 1
    Format the output as JSON with the following keys:summary:string,polarity:float.
    """
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    res = chat(chat_prompt.format_prompt(text=body).to_messages()).json()
    
    try:
        op = json.loads(json.loads(res)['content'])
    except json.JSONDecodeError:
        try:
            op = json.loads(res)['content']
            op = json.loads(op[:op.find('}') + 1])
            return op['summary'], op['polarity']
        except json.JSONDecodeError:
            print(res)
            return res['content'], res['polarity']
        
    return op['summary'], op['polarity']

def getSentiment(body):
    
    print("Analyzing Text...")
    
    template="""
    You are a helpful assistant that gives the sentiment polarity in the scale -1 to 1 for {text}
    Format the output as JSON with the following key:polarity:float.
    """
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    res = chat(chat_prompt.format_prompt(text=body).to_messages()).json()
    
    try:
        op = json.loads(json.loads(res)['content'])
    except json.JSONDecodeError:
        try:
            op = json.loads(res)['content']
            op = json.loads(op[op.find('{'):op.find('}') + 1])
            return op['polarity']
        except json.JSONDecodeError:
            newres = extract_numbers(json.loads(res)['content'])
            # print(newres)
            return newres
        
    return op['polarity']


def generateSSfromYTDescription(title, description):
    print("Analyzing Title and Description...")
    
    if title=="" or description=="":
        print("Not able to fetch title & description")
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""You are a helpful assistant that gives the sentiment polarity by analyzing the {title} and {description} of the youtube video in the scale -1 to 1.Format the output as JSON with the following keys:summary:string,polarity:float.

ignore chunks of text that contain the following:
- social media links
- shopping links
- equipment information
- copyrights
- music used
- sponsors
- discount and offers
- timestamps""",
        max_tokens=1000,
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1,
        stop=None
    )

    
    res = response.choices[0].text.strip()
    res = str(res)
    lines = res.split('\n')

    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    json_data = json.dumps(data)

    data = json.loads(json_data)

    summary = data['"summary"']
    polarity = data['"polarity"']
    
    return summary, polarity
        
# res = getSentiment("House Minority Leader Jeffries made an extreme accusation that Democrats had saved America from a right-wing plot to crash the economy, prompting Elon Musk to ask what Republicans were doing to crash the economy; Jeffries did not respond, sparking a public conversation on Twitter.")
# print(res)

