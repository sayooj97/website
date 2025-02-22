from gpt4all import GPT4All
import pandas as pd

model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name, allow_download=True)  # Ensures the model is downloaded if missing
input_file = "first_100_comments.csv"
output_file = "comments_with_sentiment.csv"
df = pd.read_csv(input_file)
sentiments = []
with model.chat_session():
     for comment in df['cleaned_comment']:
        prompt = f"Analyze the sentiment of this comment: '{comment}'. Reply with postive and negative socre.If the score is positive then reply with positve sign and score if the score is negative then reply with negative sign score"
        response = model.generate(prompt, max_tokens=20).strip().lower()
        sentiments.append(response)

# Add sentiment results to DataFrame
df['score'] = sentiments

# Save the results
df.to_csv(output_file, index=False)

print(f"Sentiment analysis completed. Results saved to {output_file}.")