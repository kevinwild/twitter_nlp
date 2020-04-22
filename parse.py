import json
import nltk
import operator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# --- NLTK --
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words("english"))  # __ Declare stop words
stop_punc = ['@', ':', 'http', 'https', '.', '!', '#', '%', ',', '?', '>', '<', '-', '&', ';']

# --- Configs ---
file_name = 'test.json'
top_word_limit = 50
# -- Global Vars ---
final_output = []
word_count = {}
top_words = 0


#  .. Load & return json file
def load_file():
    # Load json file
    with open(file_name) as f:
        return json.load(f)

#  .. Write final_output to json file
def write_file():
    k = Counter(word_count)
    # Finding n highest values
    top_words = k.most_common(top_word_limit)
    with open('final_output.json', 'w') as f:
        json.dump(top_words, f)

#  .. Loop through each tweet obj and perform analysis
def extract_info():
    for i in data:
        cleanText = handle_text(i['text'])


def handle_text(text):
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if not w in stop_words]  # __ remove stop words from text
    for word in tokens:
        if word in stop_punc:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1


data = load_file()
extract_info()
write_file()
