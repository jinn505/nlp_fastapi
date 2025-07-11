import spacy
import nltk
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

def tokenize(text : str):
    tokens = word_tokenize(text)
    filtered_tokens = [words for words in tokens if words.lower() not in stop_words and words.isalpha()]
    return filtered_tokens

def lemmatize(text : str):
    new_text = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in new_text if token.is_alpha and not token.is_stop]
    named_entities = [(ent.text, ent.label_) for ent in new_text.ents]
    return lemmatized_tokens , named_entities

def sentiment(text : str):
    response = TextBlob(text)
    sentiment_polarity = response.sentiment.polarity

    if sentiment_polarity > 0.1:
        return "happy"
    elif sentiment_polarity <-0.1:
        return "sad"
    else:
        return "neutral"
    

# import nltk
# nltk.download("punkt_tab")