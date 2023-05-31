import regex as re
import openai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.request import urlretrieve
from yt_title import get_video_info
from urllib.parse import urlencode
from eventregistry import *
from fpdf import FPDF
import config

openai.api_key = config.openAI

er = EventRegistry(allowUseOfArchive=False,
                   apiKey=config.newsAPI)

data = {'url': 'https://www.ndtv.com/india-news/watch-srks-new-parliament-building-video-has-a-touch-of-swades-4072376', 'date': '04:03:17', 'title': "Watch: SRK's New Parliament Building Video Has A Touch Of 'Swades'", 'body': 'Shah Rukh Khan has given a voice-over in the video.\n\nNew Delhi:\n\nBollywood superstar Shah Rukh Khan tweeted the video of the new parliament building that will be inaugurated by Prime Minister Narendra Modi in a grand ceremony today.\n\nShah Rukh Khan has given a voice-over in the video, with the theme music of his film \'Swades\' playing in the background.\n\n"What a magnificent new home for the people who uphold our Constitution, represent every citizen of this great Nation and protect the diversity of her one people," Shah Rukh Khan said.\n\nWhat a magnificent new home for the people who uphold our Constitution, represent every citizen of this great Nation and protect the diversity of her one People @narendramodi ji.\n\nA new Parliament building for a New India but with the age old dream of Glory for India. Jai Hind!... pic.twitter.com/FjXFZwYk2T -- Shah Rukh Khan (@iamsrk)\n\nMay 27, 2023\n\n"A new Parliament building for a New India but with the age-old dream of Glory for India. Jai Hind!" he added.\n\nPromotedListen to the latest songs, only on JioSaavn.com\n\nPrime Minister Modi responded to Shah Rukh Khan\'s tweet and said he has "beautifully expressed" the message.\n\nBeautifully expressed!\n\nThe new Parliament building is a symbol of democratic strength and progress. It blends tradition with modernity. #MyParliamentMyPridehttps://t.co/Z1K1nyjA1X -- Narendra Modi (@narendramodi)\n\nMay 27, 2023\n\nSeveral Union Ministers including Home Minister Amit Shah, Finance Minister Nirmala Sitharaman, BJP leaders have tweeted the video of the new parliament building as well. Actor Akshay Kumar also tweeted the video, with a voice-over.\n\nProud to see this glorious new building of the Parliament. May this forever be an iconic symbol of India\'s growth story. #MyParliamentMyPridepic.twitter.com/vcXfkBL1Qs -- Akshay Kumar (@akshaykumar)\n\nMay 27, 2023\n\nThe parliament building will be inaugurated by Prime Minister Narendra Modi today in a ceremony which is expected to begin at around 7 in the morning with a havan. Several dignitaries, politicians and religious heads will be present at the event.\n\nOn the day of the historic event, Prime Minister Narendra Modi will also launch a Rs 75 coin and a stamp to commemorate the inauguration of the building.', 'summary': 'Bollywood superstar Shah Rukh Khan has given a voice-over for a video of the new Parliament building that will be inaugurated by Prime Minister Narendra Modi today. Several Union Ministers and BJP leaders have also tweeted the video with a voice-over. PM Modi has responded saying Shah Rukh has "beautifully expressed" the message. The Parliament building is a symbol of India\'s progress and blends tradition with modernity. It will be inaugurated with a havan and the launch of a Rs 75 coin and stamp.', 'filename': './ss/0.jpeg'}

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
    analytics = Analytics(er)
    response = analytics.extractArticleInfo(link)
    return response


def getSnapshot(link, id):
    filename = "./ss/" + str(id) + ".jpeg"
    print("taking snap")
    params = urlencode(dict(access_key="99bfc0bf46404d9b98856a50ed23ae4a",
                        url=link
                        
                        ))
    urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params, filename )
    
    return filename


def generateSummary(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="You are an english news and video summarizer bot with the content given below and the summary of the content given above Generate a short summary in exactly 60 words no more no less. Use professional language and keep in mind this is used for Sentiment Analysis : \n" + text,
        max_tokens=1000,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=1,
        stop=None
    )
    summary = response.choices[0].text.strip()
    return summary


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
    return generateSummary(body)


def getNewsData(id, data):
    url = data['url']
    date = data['date']
    title = data['title']
    filename = getSnapshot(url, id)
    body = data['body']
    summary = getNewsSummary(body)

    return {
        'url': url,
        'date': date,
        'title': title,
        'body': body,
        'summary': summary,
        'filename': filename
    }

def generate_pdf(title, summary, link, filename):
    print("HEHEHEHE", summary)
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
    pdf.set_margins(5, 5, 5)

    # pdfname= title+'.pdf'
    pdf.output("report.pdf")

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
        generate_pdf(data['title'], data['summary'], data['url'], data['filename'])
        print(data)
