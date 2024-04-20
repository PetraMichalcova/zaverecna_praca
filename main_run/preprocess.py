import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')

file_path = 'input_dataset.csv'
df = pd.read_csv(file_path, sep=';', encoding='windows-1250')
articles = df['OBSAH'].tolist()
articles_preprocessed = []

def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text) 

for article in articles:
    preprocessed_article = article.replace('\n', ' ')
    preprocessed_article = preprocessed_article.lower()
    preprocessed_article = remove_stopwords(preprocessed_article)
    
    articles_preprocessed.append(preprocessed_article)

df['PREDSPRACOVANY'] = articles_preprocessed
df.to_csv('dataset_predspracovany.csv', sep=';', index=False)
