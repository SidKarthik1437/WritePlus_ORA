from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import newspaper
from docx import Document
from docx.shared import Inches

def is_biography_page(url):
    biography_keywords = ["wiki", "biography", "profile", "about", "tag", "topic"]
    
    for keyword in biography_keywords:
        if keyword in url.split('/')[3].lower():
            return True
    
    return False

def is_socials(url):
    
    socials = ['instagram', 'facebook']
    for key in socials:
        if key in url.split('/')[2].lower():
            return True
        
    return False

def extract_news_content(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    
    title = article.title.encode('utf-8')
    body = article.text.encode('utf-8')
    date = article.publish_date
    
    print("News Fetched!")
    
    return {'title' :title, 'body':body, 'date':date}

def get_video_info(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
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

api_key = "AIzaSyBMpLFsUCmJI1dSW1YM2ZHEZ5JHYGsjRCM"

def generate_docx(id, title, summary, sentiment, link, filename):
    # Adding a paragraph
    
    document = Document()
    
    document.add_paragraph(str(title))
    document.add_picture(filename, width=Inches(220), height=Inches(150))
    document.add_paragraph(link)
    document.add_paragraph(summary)
    document.add_paragraph(str(sentiment))
    document.save(f"./reports/{id}.docx")