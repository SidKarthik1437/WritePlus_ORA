# import regex as re
import openai
import streamlit as st

from serpapi import GoogleSearch

from eventregistry import *


import config
from helpers import *
from gs import *
from lang import *

openai.api_key = config.openAI
GoogleSearch.SERP_API_KEY = config.serpAPI


def getNewsData(id, data, url):
    # date = data['date']
    title = data['title']
    body = data['body'].decode('utf-8')
    summary = Summarizer(body)
    sentiment = getSentiment(summary)
    filename = getSnapshot(url, id, 'N')

    return {
        'type': "N",
        'body': body,
        'title': title.decode("utf-8"),
        'summary': str(summary),
        'sentiment': str(sentiment),
        'filename': filename
    }

def getYtData(id, data):
    
    flag = 0
    transcript = ""
    videoId = extractVideoId(data.get('link'))
    
    try:
        transcript = getVideoTranscript(videoId)
        
    except Exception as e:
        print(f"Cannot get transcript using title and description instead")
        flag = 1
        
    try:
        if not transcript == "" and flag == 0:
            print("Analyzing Transcript")
            summary = Summarizer(transcript)
            sentiment = getSentiment(summary)
        else: 
            summary, sentiment = generateSSfromYTDescription(data.get('title'),data.get('description'))
    except Exception as e:
        print("Summary and Sentiment ERROR!", e)    
        summary = ""
        sentiment = ""
        
        
    try:
        filename = getSnapshot(data.get('link'), id, 'Y')
    except Exception as e:
        print(f"Error occurred during snapshot retrieval: {str(e)}")
        filename = ""
    
    return {
        'type' : 'Y',
        'title': data.get('title'),
        
        'summary': summary,
        'sentiment': sentiment,
        'filename': filename,
        'published': str(data.get('published'))
    }


    
    
def googleSearchResults(keyword, max):
    
    search_results = []
    
    for res in formatResults(fetch_news_results(keyword, max)):
        
        if is_socials(res) == False:
            if not is_biography_page(res):
                search_results.append(res)
            
    return search_results

def News(keyword, max):
    export = []
    print("Fetching Google Search Results...")
    res = googleSearchResults(keyword, max)
    print("Total Links Found: ", len(res))

    for id, news in enumerate(res):
        print("Processing News: ", id)
        try:
            print("Fetching News From ", news)
            res = extract_news_content(news)
            if not res == "False":
                data = getNewsData(id, res, news)
                print("News Data Fetched")
                # generate_docx(data['type'], str(id), data['title'], data['summary'], data['sentiment'], news, data['filename'])
                export.append({'type': data['type'],'id': str(id),'title': data['title'],'summary': data['summary'],'sentiment': data['sentiment'],'link': news,'filename': data['filename']})
            else: continue
        except KeyboardInterrupt:
            exit(0)
            
    return export

def Youtube(keyword):
    yt = []
    print("Extracting Relavant Youtube Videos...")
    data = getYoutubeLinks(keyword)
    print("Total Youtube Links Found: ", len(data))

    for id, i in enumerate(data):
        print("Processing Youtube Video: ", id)
        
        try:
            print("Fetching Youtube Data...")
            data = getYtData(id, i)
            flag = 0
            for key in ["video song", "music video", "full video", "lyric video", "song"]:
                if key in i.get('title').lower():
                    flag = 1
                    break
            if flag == 1:
                continue
                
                
            print("Youtube Data Fetched")
            
            yt.append({'type': data['type'],'id': str(id),'title': data['title'],'summary': data['summary'],'sentiment': data['sentiment'],'link': i.get('link'),'filename': data['filename']})
            # generate_docx(data['type'], str(id), data['title'], data['summary'], data['sentiment'], i.get('link'), data['filename'])
                        
        except KeyboardInterrupt:
            exit(0)
                
    return yt


def main():
    
    flag = False
    
    st.title("ORAAAAAAAA")
    keyword = st.text_input("Enter Keyword")
    if st.button(label='Analyze!'):
        news = News(keyword, 20)
        # yt = Youtube(keyword)
        # generateReport(news+yt, keyword)
        generateReport(news, keyword)
        flag = True
    
    if flag == True:
        filename="./reports/"+keyword.lower()+".docx"
        with open(filename, "rb") as fp:
            st.download_button(label='Download Report', data=fp, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", file_name=f"{keyword}.docx")
    
        
if __name__ == "__main__":
    
    main()
    
