import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import pyperclip

import config
from serpapi import GoogleSearch
negative_words=['Review','Fraud','Scam','Cheat','Jail', 'Complaint', 'Scandal', 'Complaints', 'Accused', 'Cheater', 'Prosecuted', 'Ban', 'Banned', 'Arrest', 'Forgery']
def extendedResults(keyword, country, num_results):
    res = []

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
        for i in results['organic_results']:
            print(i['link'])
            res.append(i['link'])

    return res

res = extendedResults("hdfc bank pushpal roy ", 'in', 500)