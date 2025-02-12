import pandas as pd
from google import genai

genai.Client(api_key="AIzaSyBnJPhIy8E9gzrQkHObiRmRtuooOk_05k0")

df = pd.read_csv("cleaned_reddit_comments.csv")  # Load CSV file

def analyze_sentiment(review_text):  # Function receives 'review_text' (one review)
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
    Analyze the sentiment of this product review and classify it as:
    - Positive
    - Neutral
    - Negative

    Review: "{review_text}"
    
    Only return one word as output (Positive, Neutral, or Negative).
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()


# def extract_issues(review_text):
    # model = genai.GenerativeModel("gemini-pro")
# 
    # prompt = f"""
    # Analyze this PC part review and extract key issues related to:
    # - Compatibility
    # - Performance
    # - Build Quality
    # - Customer Support
# 
    # Review: "{review_text}"
# 
    # Return a csv file with categories and extracted issues.
    # """
# 
    # response = model.generate_content(prompt)
    # return response.text.strip()


# Apply sentiment analysis to each row
df["sentiment"] = df["cleaned_comment"].apply(lambda review: analyze_sentiment(str(review)))

df.to_csv("reviews_with_sentiment.csv", index=False)  # Save results

df.to_csv("reviews_with_sentiment.csv", index=False)
print("Sentiment analysis completed and saved to reviews_with_sentiment.csv")
