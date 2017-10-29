from flask import Flask
from flask import request
import pickle
import re

from nltk.corpus import stopwords # Import the stop word list
from nltk.tag import StanfordNERTagger
from nltk import word_tokenize

import json

app = Flask(__name__)
with open("forest.pkl", 'rb') as pickle_file:
    classification_model = pickle.load(pickle_file)
with open("vectorizer.pkl", 'rb') as pickle_file:
    vectorizer = pickle.load(pickle_file)
with open("doc2vec.pkl", 'rb') as pickle_file:
    doc2vec = pickle.load(pickle_file)
with open("emails.pkl", 'rb') as pickle_file:
    emails = pickle.load(pickle_file)


# Add the jar and model via their path (instead of setting environment variables):
jar = './stanford-ner.jar'
model = './edu/stanford/nlp/models/ner/german.conll.hgc_175m_600.crf.ser.gz'

ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')



def sentence_to_words(raw_sentence):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and
    # the output is a single string (a preprocessed movie review)
    #
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z0-9\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00df]", " ", raw_sentence)
    #letters_only = raw_sentence
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("german"))
    #
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    #
    # 6. Join the words back into one string separated by space,
    # and return the result.
    return(meaningful_words)

@app.route('/classify', methods=["GET"])
def classify():
    text = request.args.get("text")
    features = vectorizer.transform([" ".join(sentence_to_words(text))])
    y_pred = classification_model.predict(features)
    return y_pred[0], 200

@app.route('/locations', methods=["GET"])
def locations():
    text = request.args.get("text")
    tags = ner_tagger.tag(word_tokenize(text))
    results = [t[0] for t in tags if t[1] == "I-LOC"]
    return json.dumps(results), 200

@app.route('/similar', methods=["GET"])
def similar():
    text = request.args.get("text")
    tokens = sentence_to_words(text)
    new_vector = doc2vec.infer_vector(tokens)
    best = doc2vec.docvecs.most_similar([new_vector])[0][0]
    index = int(re.findall(r'\d+', best)[0])
    return emails[index], 200


def main():
    app.run(host='0.0.0.0', debug=False, port=8080)

if __name__ == "__main__":
    main()
