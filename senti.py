from textblob import TextBlob

def get_sentiment_scores(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (Negative) to +1 (Positive)
    if polarity > 0:
        return polarity, 0  # Positive, Negative
    elif polarity < 0:
        return 0, abs(polarity)  # Positive, Negative
    else:
        return 0, 0  # Neutral

text = "The Ryzen 7 5800X is great for gaming, but it runs too hot."
positive, negative = get_sentiment_scores(text)
print(f"Positive: {positive}, Negative: {negative}")
