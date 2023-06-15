# import regex as re
import openai
import streamlit as st

from serpapi import GoogleSearch

from eventregistry import *
import plotly.figure_factory as ff
import plotly.express as px

# import config
from helpers import *
from gs import *
from lang import *

openai.api_key = st.secrets('openAI')
GoogleSearch.SERP_API_KEY = st.secrets('serpAPI')


def getNewsData(id, data, url, keyword):
    # date = data['date']
    title = data['title']
    body = data['body'].decode('utf-8')
    summary = Summarizer(body)
    sentiment = getSentiment(summary)
    filename = getSnapshot(url, id, 'N', keyword)

    return {
        'type': "N",
        'body': body,
        'title': title.decode("utf-8"),
        'summary': str(summary),
        'sentiment': str(sentiment),
        'filename': filename
    }

def getYtData(id, data, keyword):
    
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
        filename = getSnapshot(data.get('link'), id, 'Y', keyword)
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
    with st.spinner("Analyzing News..."):
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
                    data = getNewsData(id, res, news, keyword)
                    print("News Data Fetched")
                    # generate_docx(data['type'], str(id), data['title'], data['summary'], data['sentiment'], news, data['filename'])
                    export.append({'type': data['type'],'id': str(id),'title': data['title'],'summary': data['summary'],'sentiment': data['sentiment'],'link': news,'filename': data['filename']})
                else: continue
            except KeyboardInterrupt:
                exit(0)
                
        return export

def Youtube(keyword, max, loc):
    with st.spinner('Analyzing Videos'):
        yt = []
        print("Extracting Relavant Youtube Videos...")
        data = getYoutubeLinks(keyword, max, loc)
        print("Total Youtube Links Found: ", len(data))

        for id, i in enumerate(data):
            print("Processing Youtube Video: ", id)
            
            try:
                print("Fetching Youtube Data...")
                data = getYtData(id, i, keyword)
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

import time
import numpy as np
import pandas as pd
def chartGen(data):
    fig = px.bar(data, x="id", y="sentiment", title="Polarity Graph")
    return fig 

def main():
    
    flag = False
    with open('./gl.json', 'r') as file:
        loc_data = json.load(file)
        
    loc = [i['country_name'] for i in loc_data]
    
    
    st.set_page_config(page_title="Online Reputation Analysis", page_icon="📊")
    
    st.title("📊 ONLINE REPUTATION ANALYSIS")
    keyword = st.text_input("Enter Keyword", help="Enter the prospect of interest")
    filename="./reports/"+keyword.lower()+".docx"
    col1, col2, col3 = st.columns(3)
    with col1:
        max_news = st.number_input("Max Articles", value=50 ,step=1,  min_value=10, max_value= 1000, help="More the value greater the time it takes. \n Note: These results will be filtered.")
    with col2:
        max_videos = st.number_input("Max Videos",value=10, step=1,  max_value= 100, help="More the value greater the time it takes.")
    with col3:    
        loc = st.selectbox("Location", options=loc,help="country of search", index=98 )
    # if not os.path.exists(filename):

    
    if st.button(label='Analyze!'):
            
        bar = st.progress(0, "Searching the internet")
        bar.progress(10, "Analyzing News...")
        news = News(keyword, max_news)
        bar.progress(50, "Analyzing Youtube Videos")
        yt = Youtube(keyword, max_videos, loc)
        bar.progress(90, "Generating Report")
        data = news+yt
        
        # with open("data.json", "w") as f:
        #     f.write(data)
        
        with st.spinner("Collating Data"):
            generateReport(data, keyword)
        bar.progress(100, "Report Generated!")
        time.sleep(4)
        flag = True   
    # else: flag = True
    
    
    if flag == True:
        st.balloons()
        # st.success("Report Generated!")
        
        x = pd.DataFrame([[i['id'], i['sentiment']] for i in data], columns=['id','sentiment'])
        chart = chartGen(x)
        # st.write(x)
        # st.line_chart(x, x="id", y="sentiment", )
        st.divider()
        # mean = x['sentiment'].mean() 
        # st.markdown(f"""
        #         Average polarity score &nbsp; <span style='padding: 6px; background-color: green; display: inline-block; border-radius: 10px'>{mean}</span>
        #         """, unsafe_allow_html=True)
        st.plotly_chart(chart)
    
        with open(filename, "rb") as fp:
            st.download_button(label='Download Report', data=fp, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", file_name=f"{keyword}.docx")

if __name__ == "__main__":
    
    main()
    
