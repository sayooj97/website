import re
import string
import nltk
import pandas as pd
import emoji
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from contractions import contractions_dict

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to expand contractions
def expand_contractions(text, contractions_dict=contractions_dict):
    for word, expanded in contractions_dict.items():
        text = re.sub(r'\b' + re.escape(word) + r'\b', expanded, text)
    return text

# Function to clean text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # Remove Unicode characters and emojis
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = emoji.replace_emoji(text, replace="")
    
    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()
    
    # Expand contractions
    text = expand_contractions(text)
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenization
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Rejoin words into cleaned text
    return ' '.join(words)

# Process CSV file
def process_csv(input_file, output_file):
    clean = pd.DataFrame()
    df = pd.read_csv(input_file)
    clean['comment'] = df['Comment Body']
    clean['cleaned_comment'] = df['Comment Body'].apply(clean_text)
    clean.to_csv(output_file, index=False)

# Example usage
if __name__ == "__main__":
    input_file = "reddit_comments.csv"
    output_file = "cleaned_reddit_comments.csv"
    process_csv(input_file, output_file)
    print(f"Processed data saved to {output_file}")
