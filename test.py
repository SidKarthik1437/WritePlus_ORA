data = [
  {
    "type": "N",
    "id": "N_0",
    "title": "Twitter vs India: Jack Dorsey, Elon Musk disagree on many things but seemingly agree on India",
    "summary": " Both Elon Musk and Jack Dorsey, current and former CEOs of Twitter, have expressed similar opinions on the difficulty of operating in India due to the government's strict controls. Dorsey claims the government had threatened to shut down their offices there. An Indian minister denied this, however. Twitter is also facing similar issues in Turkey and Nigeria. Since Musk fired most of Twitter's Indian staff, the company only has a handful of employees in the country and, when media inquiries are made, Twitter responds with an automated poop emoji instead of a comment.",
    "sentiment": "-0.4",
    "link": "https://www.indiatoday.in/technology/news/story/twitter-vs-india-jack-dorsey-elon-musk-disagree-on-many-things-but-seemingly-agree-on-india-2392589-2023-06-13",
    "filename": "./ss/N_0.jpeg"
  },
  {
    "type": "N",
    "id": "N_1",
    "title": "Arc of chill: Jack Dorsey poster to farmers protest to Elon Musk’s new line",
    "summary": "\n\nTwitter has had a contentious relationship with the Indian government, stemming from initial controversies in 2018 and escalating to an ultimatum in 2021 for the company to comply with multiple IT Rules. When Twitter continued to be non-compliant, they were sued and threatened with their safe harbour protections by the IT Ministry. Opposition condemned Twitter and Elon Musk stepped in to avert any further consequences.",
    "sentiment": "-0.2",
    "link": "https://indianexpress.com/article/explained/explained-sci-tech/arc-of-chill-jack-dorsey-poster-to-farm-protest-to-elon-musks-new-line-8661434/",
    "filename": "./ss/N_1.jpeg"
  }
]

y = []

for i in data:
    y.append(i['sentiment'])
    
print(y)
import pandas as pd

x = pd.DataFrame([[i['id'], i['sentiment']] for i in data], columns=['id','sentiment'])

print(x)