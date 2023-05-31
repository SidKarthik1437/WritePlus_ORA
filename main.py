from eventregistry import *
from selenium import webdriver
import openai
import regex as re
from youtube_transcript_api import YouTubeTranscriptApi
from Screenshot.Screenshot import Screenshot
from PIL import Image
from webdriver_manager.firefox import GeckoDriverManager


openai.api_key = "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"

er = EventRegistry(allowUseOfArchive=False,
                   apiKey='d14723a4-7ecc-48e0-9195-e1693735a9f2')


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


def getSnapshot(link, path):

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(link)

    def S(X): return driver.execute_script(
        'return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'), S('Height'))
    driver.find_element(by="tag", value="body").screenshot_as_png("asdfa.png")


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


def getNewsSummary(body):
    return generateSummary(body)


def getNewsData(id, data, snapPath):
    url = data.url
    date = data.date
    title = data.title
    getSnapshot(url, snapPath)
    body = data.body
    summary = data.getNewsSummary(body)
    sentimentScore = data.sentiment

    return {id, url, date, title, summary, sentimentScore, snapPath}


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
        # data = getNewsData(idx, news, snapPath="res.png")
        getSnapshot(link, path="res.png")
        # summary = generateSummary(news['body'])
        print(summary)
