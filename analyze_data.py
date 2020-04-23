import json
import nltk
import settings
from collections import Counter
import emoji
from os import path
# .. import NLTK modules
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples  # .. Used to train AI for sentiment test
from nltk import FreqDist, classify, NaiveBayesClassifier
import sys


class AnalyzeData:
    def __init__(self):
        self.file = None
        self.report = None
        self.stop_words = set(stopwords.words("english"))
        self.stop_punc = ['@', ':', 'http', 'https', '.', '!', '#', '%', ',', '?', '>', '<', '-', '&', ';']
        self.word_count = {}
        self.emoji_count = {}
        self.base_path = settings.CONFIG.get('data_store_dir') + '/'

    #  .. orchestrate report actions
    def generate_report(self):
        # ..Loop through each tweet
        for tweet in self.file:
            # .. Tokenize tweet for evaluation
            tokenized_text = self.tokenize(tweet['text'])

        # .. Compile report
        print(self.emoji_count)
        self.report = self.word_count
        #self.write_file()

    #  .. Load & return json file
    def load_file(self):
        with open(self.base_path + settings.CONFIG.get('raw_file_name'), encoding='utf-8') as f:
            self.file = json.load(f)

    # .. Write json report to file
    def write_file(self):
        with open(self.base_path + settings.CONFIG.get('report_file_name'), 'w') as f:
            json.dump(self.report, f)

    # .. Loop through teach character for unicode
    def check_emojis(self, text):
        for char in text:
            if char in emoji.UNICODE_EMOJI:
                if char not in self.emoji_count:
                    self.emoji_count[char] = 1
                else:
                    self.emoji_count[char] += 1

    # .. Break text into tokens
    def tokenize(self, text):
        # .. split text into tokens
        tweet_tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        tokens = tweet_tokenizer.tokenize(text)
        print(text)
        sys.exit()
        # .. remove stop words from tokens
        tokens = [w for w in tokens if not w in self.stop_words or w in self.stop_punc]
        # .. loop through existing tokens
        for word in tokens:
            # .. Add to word count
            if word not in self.word_count:
                self.word_count[word] = 1
            else:
                self.word_count[word] += 1
            # .. Extract Emojis
            self.check_emojis(word)

        return tokens


# .. Download dependent data for AI
def download_dependencies():
    if path.exists('.downloaded'):
        print('Dependencies Downloaded')
        return
    else:
        # .. list of un important words to be removed
        nltk.download('stopwords')
        # .. tokenizer divides a text into a list of sentences
        nltk.download('punkt')
        # .. lexical database for the English language that helps the script determine the base word
        nltk.download('wordnet')
        # .. determine the context of a word in a sentence.
        nltk.download('averaged_perceptron_tagger')
        # .. write file to directory to prove installation completion
        with open('.downloaded', 'w') as f:
            f.write('downloaded')


def train_ai():
    pass


# .. File orchestrator
def run():
    print('Analyzing data to generate final report')
    download_dependencies()
    ad = AnalyzeData()
    ad.load_file()
    ad.generate_report()


if __name__ == '__main__':
    run()
