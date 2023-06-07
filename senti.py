from textblob import TextBlob

def get_sentiment_score(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# Example usage
text = """"""

sentiment_score = get_sentiment_score(text)
print(sentiment_score)
