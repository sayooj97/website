import pandas as pd
from google import genai

# Initialize the Gemini API Client
client = genai.Client(api_key="AIzaSyBnJPhIy8E9gzrQkHObiRmRtuooOk_05k0")

# Function to analyze sentiment for a batch of comments
def analyze_batch_of_comments(batch_comments):
    results = []  # Store the sentiment analysis results
    
    for comment in batch_comments:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Analyze the sentiment of the following comment: '{comment}'"
        )
        sentiment = response.text.strip()  # Extract only the sentiment
        results.append(sentiment)
    
    return results

# Function to process comments in batches and assign sentiment to a new column
def process_comments_in_batches(csv_file, batch_size=10):
    df = pd.read_csv(csv_file)  # Load comments from CSV

    sentiments = []  # Store sentiment results

    for start in range(0, len(df), batch_size):
        batch_comments = df['cleaned_comment'][start:start + batch_size].tolist()
        batch_sentiments = analyze_batch_of_comments(batch_comments)
        sentiments.extend(batch_sentiments)

    # Assign sentiment to a new column in the DataFrame
    df["sentiment_analysis"] = sentiments

    # Save the updated DataFrame with both comments and sentiments
    df.to_csv("sentiment_results_batchwise.csv", index=False)
    print("Sentiment analysis completed and saved.")

# Run the batch processing function
process_comments_in_batches("cleaned_reddit_comments.csv", batch_size=10)
