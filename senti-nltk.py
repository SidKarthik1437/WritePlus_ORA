import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

# Create a SentimentIntensityAnalyzer object
sia = SentimentIntensityAnalyzer()

# Text to analyze
text = "I really enjoyed the movie. The acting was excellent."

# Analyze sentiment and obtain polarity scores
sentiment_scores = sia.polarity_scores(text)

# Extract the polarity score
polarity_score = sentiment_scores['compound']

# Print the polarity score
print("Polarity Score:", polarity_score)
