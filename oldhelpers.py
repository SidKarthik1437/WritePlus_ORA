
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