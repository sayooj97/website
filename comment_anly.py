import csv
from collections import defaultdict
from gpt4all import GPT4All

# Load GPT4All model
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name, allow_download=True)

# Input and output CSV filenames
input_csv = "cleaned_reddit_comments.csv"
output_csv = "reddit_pc_parts_keywords.csv"

# Dictionary to store keyword frequencies
keyword_freq = defaultdict(int)

# Open input CSV and process comments
with open(input_csv, "r", encoding="utf-8") as infile, open(output_csv, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ["comment_id", "keywords", "sentiment", "sentiment_score", "pc_part_type", "keyword_frequency", "absa_data"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()  # Write column headers

    with model.chat_session():  # GPT4All session
        for row in reader:
            comment_id = row["comment_id"]
            comment_text = row["comment"]
            sentiment = row["sentiment"]
            
            # Extract PC part keywords
            prompt_keywords = f"Extract only the relevant PC part keywords (CPU, GPU, RAM, etc.) from the following comment:\n\n{comment_text}\n\nOnly return a comma-separated list of keywords."
            keywords = model.generate(prompt_keywords, max_tokens=50).strip()
            
            # Update keyword frequency
            for keyword in keywords.split(", "):
                keyword_freq[keyword.lower()] += 1  # Store in lowercase for consistency

            # Get sentiment score (-1 to 1)
            prompt_sentiment_score = f"Assign a sentiment score between -1 (negative) to +1 (positive) for this comment:\n\n{comment_text}\n\nOnly return a number."
            sentiment_score = model.generate(prompt_sentiment_score, max_tokens=5).strip()

            # Aspect-Based Sentiment Analysis (ABSA)
            prompt_absa = f"Extract aspect-based sentiment for each keyword in this comment:\n\n{comment_text}\n\nFormat: 'keyword - sentiment'."
            absa_data = model.generate(prompt_absa, max_tokens=100).strip()

            # Determine PC part type
            if any(part in keywords.lower() for part in ["cpu", "processor"]):
                pc_part_type = "CPU"
            elif any(part in keywords.lower() for part in ["gpu", "graphics", "nvidia", "amd"]):
                pc_part_type = "GPU"
            elif any(part in keywords.lower() for part in ["ram", "memory"]):
                pc_part_type = "RAM"
            elif any(part in keywords.lower() for part in ["psu", "power supply"]):
                pc_part_type = "PSU"
            elif any(part in keywords.lower() for part in ["motherboard", "mobo"]):
                pc_part_type = "Motherboard"
            else:
                pc_part_type = "Other"

            # Write extracted data to CSV
            writer.writerow({
                "comment_id": comment_id,
                "keywords": keywords,
                "sentiment": sentiment,
                "sentiment_score": sentiment_score,
                "pc_part_type": pc_part_type,
                "keyword_frequency": sum(keyword_freq[key.lower()] for key in keywords.split(", ")),
                "absa_data": absa_data
            })

print(f"Keyword extraction, sentiment scoring, and ABSA completed. Results saved to {output_csv}.")
