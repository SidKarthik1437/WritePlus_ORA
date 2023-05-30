from eventregistry import *

er = EventRegistry(allowUseOfArchive=False,
                   apiKey='d14723a4-7ecc-48e0-9195-e1693735a9f2')


def getNewsFromKeyword(keyword):
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
    for idx, article in enumerate(q.execQuery(er, maxItems=100)):
        # title = str(article['title']).strip()[:10]
        with open("./csk/" + str(idx) + ".txt", 'w', encoding="UTF-8",) as f:
            f.write(str(article))


getNewsFromKeyword("Chennai Super Kings")
