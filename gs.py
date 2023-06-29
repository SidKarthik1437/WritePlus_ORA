import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import config
from serpapi import GoogleSearch

def fetch_news_results(keyword, num_results):
    search_results = []
    
    # Perform the Google search
    url = f"https://www.google.com/search?q={keyword}"
    response = requests.get(url)
    # print(response.content)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the news article links
    links = soup.find_all("a")
    # Extract the URLs from the links
    for link in links[:num_results]:
        url = link["href"]
        search_results.append(url)
    print(len(search_results))
    return search_results

def formatResults(results):
    res = []
    for i, result in enumerate(results):
        if result.split('?')[0] == '/search' or result.split('?')[0] == '/advanced_search' or "google.com" in result:
            continue
        else: 
            if "https://" in result:
                parsed_url = urlparse(result)
                query_params = parse_qs(parsed_url.query)
                if 'q' in query_params:
                    link = query_params['q'][0]
                    res.append(link)
    return res

negative_words=['Review','Fraud','Scam','Cheat','Jail', 'Complaint', 'Scandal', 'Complaints', 'Accused', 'Cheater', 'Prosecuted', 'Ban', 'Banned', 'Arrest', 'Forgery']

def extendedResults(keyword, country, num_results):
    res = []
    print(country)
    for word in negative_words:

        params = keyword + " " + word
        print("-------------------" + params + "-------------------", end="\n")
        params = {
        "api_key": config.serpAPI,
        "engine": "google",
        "q": params,
        "google_domain": "google.com",
        "gl": country,
        "hl": "en",
        "num": num_results
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        # print(results.get('organic_results'))
        for i in results['organic_results']:
            print(i['link'])
            res.append(i['link'])

    return res[:num_results]

