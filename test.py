import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def formatResult(url):
    
    if any(element in url for element in ['/search', '/advanced_search', 'google.com', 'lumen']):
        return None
    else: 
        return url

def fetch_news_results(keyword, num_results):
    search_results = []
    start_index = 0
    
    while len(search_results) < num_results:
        # Perform the Google search
        url = f"https://www.google.com/search?q={keyword}&start={start_index}"
        response = requests.get(url)
        
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the news article links
        links = soup.find_all("a")
        
        # Extract the URLs from the links
        for link in links:
            url = link.get("href")
            if url.startswith("/url?q="):
                url = url[7:]  # Remove the "/url?q=" prefix
                if formatResult(url) is not None:
                    search_results.append(url)
                    print(url)
        
        start_index += 10  # Increment the start index for the next page
        
    return search_results[:num_results]

# res = fetch_news_results("hdfc pushpal roy", 500)
# # print(res)
# print(len(res))

from serpapi import GoogleSearch

params = {
  "api_key": "c84207c20a9c6e6f61033d6975ef3c716f6f42e3157e02b586a8a1835be7f01f",
  "engine": "google",
  "q": "hdfc pushpal roy",
  "google_domain": "google.com",
  "gl": "in",
  "hl": "en",
  "num": "200"
}

search = GoogleSearch(params)
results = search.get_dict()
for i in results['organic_results']:
    
    print(i['link'])

print(len(results['organic_results']))