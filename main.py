import regex as re
import openai

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
    summary = lang.Summarizer(body)
    sentiment = getSentiment(summary)
    filename = getSnapshot(url, id)

    return {
        'type': "N",
        # 'date': date,
        'title': title,
        'summary': str(summary),
        'sentiment': str(sentiment),
        'filename': filename
    }

def getYtData(id, data):
    try:
        videoId = extractVideoId(data.get('link'))
        try:
            transcript = getVideoTranscript(videoId)
        except Exception as e:
            print(f"Error occurred during Transcript extraction: {str(e)}")
            summary = ""
        try:
            summary = Summarizer(transcript)
            
        except Exception as e:
            print(f"Error occurred during summary generation: {str(e)}")
            summary = ""
        
        try:
            sentiment = getSentiment(summary)
        except Exception as e:
            print(f"Error occurred during sentiment analysis: {str(e)}")
            sentiment = ""
        
        try:
            filename = getSnapshot(data.get('link'), id)
        except Exception as e:
            print(f"Error occurred during snapshot retrieval: {str(e)}")
            filename = ""
        
        return {
            'type' : 'Y',
            'title': data.get('title'),
            'summary': str(summary),
            'sentiment': str(sentiment),
            'filename': filename,
            'published': str(data.get('published'))
        }
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def googleSearchResults(keyword):
    
    search_results = []
    
    for res in formatResults(fetch_news_results(keyword, 20)):
        
        if is_socials(res) == False:
            if not is_biography_page(res):
                search_results.append(res)
            
    return search_results

def News(keyword):
    print("Fetching Google Search Results...")
    res = googleSearchResults(keyword)
    print("Total Links Found: ", len(res))

    for id, news in enumerate(res):
        print("Processing News: ", id)
        try:
            print("Fetching News From ", news)
            res = extract_news_content(news)
            if not res == "False":
                data = getNewsData(id, res, news)
                print("News Data Fetched")
                generate_docx(data['type'], str(id), data['title'], data['summary'], data['sentiment'], news, data['filename'])
            else: continue
        except KeyboardInterrupt:
            exit(0)

def Youtube(keyword):
    print("Extracting Relavant Youtube Videos...")
    data = getYoutubeLinks(keyword)
    print("Total Youtube Links Found: ", len(data))

    for id, i in enumerate(data):
        print("Processing Youtube Video: ", id)
        try:
            print("Fetching Youtube Data...")
            data = getYtData(id, i)
            print("Youtube Data Fetched")
            
            generate_docx(data['type'], str(id), data['title'], data['summary'], data['sentiment'], i.get('link'), data['filename'])
                        
        except KeyboardInterrupt:
            exit(0)


def main():
    
    keyword = 'Rahul Gandhi'
    News(keyword)
    Youtube(keyword)
    
        

if __name__ == "__main__":
    main()
    
