import json
import nltk
import settings
from collections import Counter
from collections import OrderedDict

import emoji
from os import path
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import sentiment


class AnalyzeData:
    def __init__(self):
        self.file = None
        self.report = {'total_tweets': 0, 'positive_count': 0, 'negative_count': 0,
                       'total_certain_positive': 0, 'total_certain_negative': 0,'positive_tweets': [],
                       'negative_tweets': []}
        self.stop_words = set(stopwords.words("english"))
        self.stop_punc = ['@', ':', 'http', 'https', '.', '!', '#', '%', ',', '?', '>', '<', '-', '&', ';', '?', '\''
                          '...', '\u2026', '\\', '\u2019', '\"', "'", '...', '\ufe0f', '\u201c', '(', '*', ')', '\u200d']
        self.word_count = {}
        self.emoji_count = {}
        self.strong_positive = {}
        self.strong_negative = {}
        self.twitter_tone_count = {}
        self.user_locations = {}
        self.base_path = settings.CONFIG.get('data_store_dir') + '/'
        self.sentiment = sentiment.Sentiment()

    #  .. orchestrate report actions
    def generate_report(self):
        # ..Loop through each tweet
        for tweet in self.file:
            self.report['total_tweets'] += 1
            # .. User location handle
            self.handle_user_locations(tweet['userLocation'])
            # .. Build Word Count and Emoji Count
            self.tokenize(tweet['text'])
            # .. Analyze tweet tone
            tone = sentiment.Sentiment.check_tone(self.sentiment, tweet['text'])
            # .. Check tone against confidence limit
            if tone[1] >= settings.CONFIG.get('confidence_level'):
                if tone[0] == 'Positive':
                    self.report['positive_count'] += 1
                    if tone[1] >= settings.CONFIG.get('tweet_save_limit'):
                        self.report['total_certain_positive'] += 1
                        self.report['positive_tweets'].append(return_tweet_format(tone, tweet['text']))
                else:
                    self.report['negative_count'] += 1
                    if tone[1] >= settings.CONFIG.get('tweet_save_limit'):
                        self.report['total_certain_negative'] += 1
                        self.report['negative_tweets'].append(return_tweet_format(tone, tweet['text']))

        # .. Final processing
        k = Counter(self.word_count)
        top_word_limit = settings.CONFIG.get('top_word_limit')
        self.report['top_'+str(top_word_limit)+'_words'] = k.most_common(top_word_limit)
        self.report['emoji_count'] = sorted(self.emoji_count.items(), key=lambda pair: pair[1], reverse=True)
        self.report['user_locations'] = sorted(self.user_locations.items(), key=lambda pair: pair[1], reverse=True)
        # .. Write report
        self.write_file()

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
        # .. remove stop words from tokens
        tokens = [w for w in tokens if (not w in self.stop_words)]
        # .. loop through existing tokens
        for word in tokens:
            if word in self.stop_punc:
                continue
            # .. Add to word count
            if word not in self.word_count:
                self.word_count[word] = 1
            else:
                self.word_count[word] += 1
            # .. Extract Emojis
            self.check_emojis(word)

        return tokens

    def handle_user_locations(self, geo):
        if geo in self.user_locations:
            self.user_locations[geo] += 1
        else:
            self.user_locations[geo] = 1
    # .. END .. AnalyzeData Class


# .. Format tweet for report json
def return_tweet_format(tone, text):
    return {'confidence': tone[1], 'tweet': text}


# .. Download dependent data for AI
def download_dependencies():
    if path.exists('.downloaded'):
        print('Dependencies Downloaded')
        return
    else:
        # .. download twitter samples
        nltk.download('twitter_samples')
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


# .. File orchestrator
def run():
    print('Analyzing data to generate final report')
    download_dependencies()
    ad = AnalyzeData()
    ad.load_file()
    ad.generate_report()


if __name__ == '__main__':
    run()
