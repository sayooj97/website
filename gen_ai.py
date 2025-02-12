import pandas as pd
from google import genai

# Initialize the client for Gemini API
client = genai.Client(api_key="AIzaSyBnJPhIy8E9gzrQkHObiRmRtuooOk_05k0")

# Load the CSV file (Ensure the CSV has 'comment' column)
df = pd.read_csv("cleaned_reddit_comments.csv")

# Function to analyze sentiment using the official model
def analyze_sentiment(comment):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Analyze the sentiment of the following comment: '{comment}'"
    )
    return response.text.strip()

# Apply sentiment analysis to each comment
df["sentiment_analysis"] = df["cleaned_comment"].apply(analyze_sentiment)

# Save the results to a new CSV file
df.to_csv("sentiment_results.csv", index=False)

print("Sentiment analysis completed and saved.")
