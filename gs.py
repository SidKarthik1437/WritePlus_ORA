import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def fetch_news_results(keyword, num_results):
    search_results = []
    
    # Perform the Google search
    url = f"https://www.google.com/search?q={keyword}&tbm=nws"
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
    
    return search_results

# Example usage

# Print the search results
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

# https://indianexpress.com/article/trending/trending-in-india/man-who-lives-in-jharkhand-is-a-shah-rukh-khan-doppelganger-from-earlier-days-8648722/
# https://indianexpress.com/article/trending/trending-in-india/man-who-lives-in-jharkhand-is-a-shah-rukh-khan-doppelganger-from-earlier-days-8648722/&sa=U&ved=2ahUKEwi8xNje1bD_AhUEH7kGHaVjC6YQxfQBegQIBhAC&usg=AOvVaw00JFLC86KwWjVu7EV5qqTD