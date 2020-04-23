import json
import nltk
import settings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import emoji


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
        self.emoji_count = {}
        self.base_path = settings.CONFIG.get('data_store_dir') + '/'

    #  .. orchestrate report actions
    def generate_report(self):
        # ..Loop through each tweet
        for tweet in self.file:
            # .. Extract Emojis
            self.check_emojis(tweet['text'])
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

    def write_file(self):
        with open(self.base_path + settings.CONFIG.get('report_file_name'), 'w') as f:
            json.dump(self.report, f)

    def check_emojis(self, text):
        for char in text:
            if char in emoji.UNICODE_EMOJI:
                if char not in self.emoji_count:
                    self.emoji_count[char] = 1
                else:
                    self.emoji_count[char] += 1

    def tokenize(self, text):
        # .. split text into tokens
        tokens = word_tokenize(text)
        # .. remove stop words from tokens
        tokens = [w for w in tokens if not w in self.stop_words or w in self.stop_punc]
        # .. loop through existing tokens
        for word in tokens:
            # .. Add to word count
            if word not in self.word_count:
                self.word_count[word] = 1
            else:
                self.word_count[word] += 1

        return tokens




def run():
    ad = AnalyzeData()
    ad.load_file()
    ad.generate_report()


if __name__ == '__main__':
    run()
