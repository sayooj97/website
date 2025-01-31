import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

num_topics = 10

lda = LatentDirichletAllocation(n_components=num_topics,random_state=42)

df = pd.read_csv("cleaned_text.csv")
reviews = df['comments'].dropna().tolist()


vectiorizer = TfidfVectorizer(max_features=500, stop_words='english')
tfidf_matrix = vectiorizer.fit_transform(reviews)
keywords = vectiorizer.get_feature_names_out()
lda.fit(tfidf_matrix)

words = keywords

for topic_idx, topic in enumerate(lda.components_):
    top_keywords = [words[i] for i in topic.argsort()[-10:]]
    print(f"Topic{topic_idx+1}:{', '.join(top_keywords)}")


print("Top keywords from reviews :",keywords)