import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Load stopwords
stop_words = set(stopwords.words('english'))

def preprocess_text(comment):
    # Lowercase the text
    comment = comment.lower()
    # Remove punctuation and special characters
    comment = re.sub(r'[^a-zA-Z0-9\s]', '', comment)
    # Tokenize the text
    tokens = word_tokenize(comment)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize to reduce words to their base form
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Join tokens back into a single string
    return ' '.join(tokens)

# Example usage
# example_comment = "Good for gaming, compatible with AM4 boards this is too bad!"
# cleaned_comment = preprocess_text(example_comment)
# print("Cleaned Comment:", cleaned_comment)

file_comment = pd.read_csv("comment_reddit.csv")
print(file_comment.head())
cleaned_data = pd.DataFrame()
cleaned_related_parts = pd.DataFrame();
cleaned_data['related_parts'] = file_comment['related_parts']
cleaned_data['comments'] = file_comment['comment_text'].apply(preprocess_text)

# file_comment['cleaned_text'] = file_comment['comment_text'].apply(preprocess_text)

to_print = cleaned_data.to_csv('cleaned_text.csv', index=False)

clean = pd.read_csv("cleaned_text.csv")
print(clean.head())