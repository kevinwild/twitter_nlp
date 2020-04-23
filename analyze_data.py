import json
import nltk
import settings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# --- NLTK -- Update || Download --
nltk.download('stopwords')
nltk.download('punkt')


class AnalyzeData:
    def __init__(self):
        self.file = None
        self.report = None
        self.stop_words = set(stopwords.words("english"))
        self.stop_punc = ['@', ':', 'http', 'https', '.', '!', '#', '%', ',', '?', '>', '<', '-', '&', ';']
        self.word_count = {}

    #  .. orchestrate report actions
    def generate_report(self):
        # ..Loop through each tweet
        for tweet in self.file:
            # .. Tokenize tweet for evaluation
            tokenized_text = self.tokenize(tweet['text'])

    #  .. Load & return json file
    def load_file(self):
        with open(settings.CONFIG.get('data_store_dir') + '/' + settings.CONFIG.get('raw_file_name')) as f:
            self.file = json.load(f)

    #  .. Create tokenized word obj and remove stop words also during tokenizing process add valid words to word_count
    def tokenize(self, text):
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if not w in self.stop_words]  # __ remove stop words from text
        for word in tokens:
            if word in self.stop_punc:
                continue
            if word not in self.word_count:
                self.word_count[word] = 1
            else:
                self.word_count[word] += 1


def run():
    ad = AnalyzeData()
    ad.load_file()
    ad.generate_report()


if __name__ == '__main__':
    run()
