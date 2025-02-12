import re
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np

# Download NLTK tokenizer
nltk.download("punkt")

# Load pre-trained RoBERTa model for sentiment analysis
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Sentiment labels
sentiment_labels = ["negative", "neutral", "positive"]

# List of PC parts for identification
pc_parts = ["CPU", "GPU", "motherboard", "RAM", "PSU", "SSD", "HDD", "cooler", "fan", "case", "monitor"]

# Sample dataset with mixed sentiments
comments = [
    "The RTX 4070 is an amazing GPU! Super fast and efficient. But my PSU is awful, it died in 2 months.",
    "This CPU overheats way too much, terrible for gaming. But the motherboard is solid and reliable!",
    "My SSD is really fast and works great. The fan noise, however, is unbearable!",
]

# Function to classify sentiment using RoBERTa
def get_sentiment(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        output = model(**tokens)
    scores = output.logits.softmax(dim=-1).numpy()[0]
    sentiment = sentiment_labels[np.argmax(scores)]
    return sentiment

# Process comments
structured_data = []

for comment in comments:
    sentences = sent_tokenize(comment)  # Split by sentence
    for sentence in sentences:
        sentiment = get_sentiment(sentence)  # Get sentiment
        related_parts = [part for part in pc_parts if part.lower() in sentence.lower()]  # Identify PC parts
        
        # If multiple parts are mentioned, store each separately
        if related_parts:
            for part in related_parts:
                structured_data.append({"Comment": sentence, "Sentiment": sentiment, "Related Part": part})
        else:
            structured_data.append({"Comment": sentence, "Sentiment": sentiment, "Related Part": "Unknown"})

# Convert to DataFrame
df = pd.DataFrame(structured_data)

# Print structured output
print(df)
