import re
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np

part_files = {
    "ram": "csv_files/memory.csv",
    "gpu": "csv_files/video-card.csv",
    "cpu": "csv_files/cpu.csv",
    "psu": "csv_files/power-supply.csv",
    "motherboard": "csv_files/motherboard.csv",
    # "ssd": "csv_files/ssd.csv",
    # "hdd": "csv_files/hdd.csv",
    "cooling": "csv_files/cpu-cooler.csv",
    "case": "csv_files/case.csv"
}

part_dict = {}

for part_type , filename in part_files.items():
    try:
        df_parts = pd.read_csv(filename)
        for part_name in df_parts.iloc[:,0]:
            part_dict[part_name.lower()] = part_type
    except FileNotFoundError:
        print(f"Warning {filename} not found, skipping.....s")

def identify_part(comment):
    if not isinstance(comment,str):
        return[(None, None)]
    comment_lower = comment.lower()
    found_part = []

    for part_name, part_type in part_dict.items():
        if part_name in comment_lower:
            found_part.append((part_name, part_type))
    if not found_part:
        for part_type in part_files.keys():
            if part_type in comment_lower:
                found_part.append((None, part_type))

    return found_part if found_part else [(None, None)]

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

def get_sentiment(comment):
    inputs = tokenizer(comment, return_tensors="pt", truncation=True,padding=True)
    with torch.no_grad():
        output = model(** inputs)
        scores = output.logits.softmax(dim=-1).numpy()[0]
        sentiment_labels = ["negative", "neutral", "positive"]
        sentiment = sentiment_labels[np.argmax(scores)]
        return sentiment

def process_comments(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    results = []

    for comment in df["cleaned_comment"].fillna(""):
        comment = str(comment)
        parts = identify_part(comment)
        if not isinstance(parts, list):
            parts = [parts]
        for part_name, part_type in parts:
            sentiment = get_sentiment(comment)
            results.append([comment, part_name, part_type, sentiment])

        df_results = pd.DataFrame(results, columns=["original_comment", "part_name", "part_type", "sentiment_label"])

        df_results.to_csv(output_csv, index=False)

# print(f"processed comments saved to {output_csv}")

if __name__ == "__main__":
    input_csv = "cleaned_reddit_comments.csv"
    output_csv = "processed_comments.csv"

    process_comments(input_csv, output_csv)