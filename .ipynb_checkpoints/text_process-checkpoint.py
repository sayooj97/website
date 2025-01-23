import re
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
example_comment = "Good for gaming, compatible with AM4 boards!"
cleaned_comment = preprocess_text(example_comment)
print("Cleaned Comment:", cleaned_comment)
