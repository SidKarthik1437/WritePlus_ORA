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
    
    flag = 0
    transcript = ""
    videoId = extractVideoId(data.get('link'))
    
    try:
        transcript = getVideoTranscript(videoId)
        
    except Exception as e:
        print(f"Cannot get transcript using title and description instead")
        flag = 1
        
    try:
        if transcript == "" and flag == 1:
            summary = Summarizer(transcript)
            sentiment = getSentiment(summary)
        else: 
            summary, sentiment = generateSSfromYTDescription(data.get('title'),data.get('description'))
    except Exception as e:
        print(e)    
        summary = ""
        sentiment = ""
        
        
    try:
        filename = getSnapshot(data.get('link'), id)
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


    
    
def googleSearchResults(keyword):
    
    search_results = []
    
    for res in formatResults(fetch_news_results(keyword, 20)):
        
        if is_socials(res) == False:
            if not is_biography_page(res):
                search_results.append(res)
            
    return search_results

def News(keyword):
    export = []
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
    
    keyword = 'narendra modi'
    # news = News(keyword)
    yt = Youtube(keyword)
    
    generateReport(yt, keyword)
    
        

if __name__ == "__main__":
    main()
    
