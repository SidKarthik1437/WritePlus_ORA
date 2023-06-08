from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import newspaper
from docx import Document
from docx.shared import Inches
from fpdf import FPDF
from textblob import TextBlob
import datetime
from serpapi import GoogleSearch

import config

def is_biography_page(url):
    biography_keywords = ["wiki", "biography", "profile", "about", "tag", "topic"]
    
    for keyword in biography_keywords:
        if keyword in url.split('/')[3].lower():
            return True
    
    return False

def is_socials(url):
    
    socials = ['instagram', 'facebook', 'youtube', 'vimeo', 'inhabitat.com', 'warwickonline']
    for key in socials:
        if key in url.lower():
            return True
        
    return False

def extract_news_content(url):
    
    try:
        
        article = newspaper.Article(url)
        article.download()
        article.parse()
    except newspaper.ArticleException:
        print("cannot fetch news for the url: ", url)
        return 
    
    title = article.title.encode('utf-8')
    body = article.text.encode('utf-8')
    date = article.publish_date
    
    print("News Fetched!")
    
    return {'title' :title, 'body':body, 'date':date}

def get_sentiment_score(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=config.youtubeAPI)
    
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        items = response.get('items', [])
        if items:
            video_info = items[0]
            print(video_info)
            title = video_info['snippet']['title']
            # thumbnail_url = video_info['snippet']['thumbnails']['default']['url']
            return title

    except HttpError as e:
        print(f'Error retrieving video info for video ID {video_id}: {e}')

    return None, None

def getYoutubeLinks(keyword):
    links = []
    params = {
            "api_key": config.serpAPI,
            "engine": "youtube",
            "search_query": keyword,
            "hl": "en",
            "gl": "in"
        }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    res = results.get('video_results')
    for i in res:
        links.append(i.get('link'))
        
    return links

def generate_docx(id, title, summary, sentiment, link, filename):
    # Adding a paragraph
    
    document = Document()
    
    document.add_paragraph(str(title))
    document.add_picture(filename, width=Inches(220), height=Inches(150))
    document.add_paragraph(link)
    document.add_paragraph(summary)
    document.add_paragraph(str(sentiment))
    document.save(f"./reports/{id}.docx")
    
def generate_pdf(id, title, summary, sentiment, link, filename):
    # print("HEHEHEHE", summary)
    print("Generating PDF for News: ", id)
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)

    pdf.cell(200, 10, "Title: " + title, align='L')

    pdf.set_font('Arial', '', 12)
    pdf.image(filename,  x=10, y=80, w=220, h=150 )
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(150, 10,  "Summary: ")
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(150, 10,  summary)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(180, 5, "URL:")
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(180, 5, link)
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(180, 5, "Polarity Score:")
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(180, 5, sentiment)
    pdf.set_margins(5, 5, 5)

    # pdfname= title+'.pdf'
    pdf.output(f"./reports/{id}.pdf")
    print("PDF ", id, " Generated!")

res = getYoutubeLinks("Apple")
print(res)
