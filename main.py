import regex as re
import openai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.request import urlretrieve
from helpers import get_video_info
from urllib.parse import urlencode

from serpapi import GoogleSearch
from googlesearch import search

from eventregistry import *


import config
import helpers
import gs
import lang

import json
import streamlit as st

openai.api_key = config.openAI
GoogleSearch.SERP_API_KEY = config.serpAPI

er = EventRegistry(allowUseOfArchive=False,
                   apiKey=config.newsAPI)
analytics = Analytics(er)


def getNewsFromKeyword(keyword, max):
    qStr = f"""
    {{
        "$query": {{
            "$and": [
                {{
                    "keyword":  "{keyword}",
                    "keywordLoc": "title"
                }},
                {{
                    "locationUri": "http://en.wikipedia.org/wiki/India"
                }},
                {{
                    "dateStart": "2023-05-23",
                    "dateEnd": "2023-05-30",
                    "lang": "eng"
                }}
            ]
        }},
        "$filter": {{
            "dataType": [
                "news",
                "pr",
                "blog"
            ]
        }}
    }}
    """
    q = QueryArticlesIter.initWithComplexQuery(qStr)
    # change maxItems to get the number of results that you want
    return q.execQuery(er, max)


def getNewsFromLink(link):
    response = analytics.extractArticleInfo(link)
    print("News From Link FETCHED! ")
    return response


def getSnapshot(link, id):
    filename = "./ss/" + str(id) + ".jpeg"
    print("taking snap")
    params = urlencode(dict(access_key="99bfc0bf46404d9b98856a50ed23ae4a",
                        url=link
                        
                        ))
    try:
        urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params, filename )
    except KeyboardInterrupt:
        exit(0)
    return filename


def generateSummary(text):
    data = {}  # Initialize data as an empty dictionary
    prompt = str(text)
    
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": "You are tasked with generating a summary of a given text in 120 words. Strictly include only the requested details and do not use double quotes in the summary."},
        ]
    )
    
   
    
    return response.choices[0].message.content
        

def extractVideoId(link):
    regex = r"(?<=v=|v\/|vi=|vi\/|youtu.be\/|embed\/|\/v\/|\/e\/|watch\?v=|\?v=|\/embed\/|\/e\/|youtu.be\/|\/v\/|watch\?v=|embed\/)[^#\\?\\&]*"
    match = re.search(regex, link)
    if match:
        return match.group(0)
    else:
        return None


def getVideoTranscript(video_id):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"Transcript for video ID {video_id}:")
        transcript = ""
        for segment in data:
            transcript += "\n" + segment['text']
    except Exception as e:
        print(f"Error occurred for video ID {video_id}: {str(e)}")

    return transcript

def getVideoTitle(video_id):
    title = get_video_info(video_id)
    return title


def getNewsSummary(body):
    print("Generating Summary...")
    return generateSummary(body)

def getSentiment(body):
    print("Analysing Sentiment...")
   
    prompt =" Return only the sentiment polarity score for the text: \n"+ str(body)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
             {"role": "system", "content": "You are tasked with generating sentiment polarity score for the given text in the scale -1 to 1. Return only the polarity score and if sentiment cannot be analysed return 0"}
            ,{"role": "user", "content": prompt}
                  ]
        
    )
    print(response.choices[0].message.content)
    sentiment = response.choices[0].message.content
    return sentiment
    

def getNewsData(id, data, url):
    date = data['date']
    title = data['title']
    body = data['body'].decode('utf-8')
    summary, sentiment = lang.ChatSummarizer(body)
    # sentiment = helpers.get_sentiment_score(body)
    filename = getSnapshot(url, id)

    return {
        'date': date,
        'title': title,
        # 'body': body,
        'summary': str(summary),
        'sentiment': str(sentiment),
        'filename': filename
    }


def googleSearchResults(keyword):
    
    search_results = []
    
    for res in search(keyword, num_results=50, lang='en'):
        
        if helpers.is_socials(res) == False:
            if not helpers.is_biography_page(res):
                search_results.append(res)
            
    return search_results

def __init__():
    print("init")
    with open("./links.txt", "r") as file:
        links = file.readlines()

    for idx, link in enumerate(links):
        if link.__contains__("youtube"):
            videoId = extractVideoId(link)
            transcript = getVideoTranscript(videoId)
            summary = generateSummary(transcript)
            print(summary)
        else:
            news = getNewsFromLink(link)
            data = getNewsData(idx, news)
            helpers.generate_docx(data['title'], data['summary'], data['url'], data['filename'])
            print(data)

def main():
    # st.title("ORA")
    # keyword = str(input("Enter Search Keyword: "))
    # keyword = st.text_input("Enter a keyword:")
    
    keyword = 'Kanva marketing fraud'
    
    print("Fetching Google Search Results...")
    res = gs.formatResults(gs.fetch_news_results(keyword, 1000))
    print("Total Links Found: ", len(res))

    for id, news in enumerate(res):
        print("Processing News: ", id)
        try:
            print("Fetching News From Link...")
            res = helpers.extract_news_content(news)
            
            data = getNewsData(id, res, news)
            print("News Data Fetched")
            helpers.generate_docx(str(id), data['title'], data['summary'], data['sentiment'], news, data['filename'])
            
        except KeyboardInterrupt:
            exit(0)
        
        
             

if __name__ == "__main__":
    main()
    
