import re
import pandas as pd

# Define comparison phrases
comparison_phrases = [
    r"prefer (.*) to",
    r"(.*) is better (.*)",
    r"(.*) performs worse (.*)"
]

# Function to extract comparison relationships
def extract_comparison(comment):
    if not isinstance(comment,str):
        return None
    for phrase in comparison_phrases:
        match = re.search(phrase, comment, re.IGNORECASE)
        if match:
            return match.group()  # Return the matching phrase
    return None

# Example
comment = pd.read_csv("cleaned_text.csv")
file = pd.DataFrame()
file['comparison'] = comment['comments'].apply(extract_comparison)
# print(extract_comparison(comment))
file.dropna(subset=['comparison'], inplace=True)
file.to_csv('comparison.csv',index=False)