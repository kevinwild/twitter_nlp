#  ..
#  .. This class is going to do a supervised classification for positive and negative tweets
#  .. After ML training the class will return the result of a tweet passed to the examine method
#  .. and will return a result negative, neutral or positive tone towards the tweet
#  .. -- dependencies are downloaded in analyze_data file
#  .. -- this class was based from the following article:
#  .. -- https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
#  ..
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random
import sys


class Sentiment:
    def __init__(self):
        self.clean_positive = []
        self.clean_negative = []
        self.freq_dist_pos = None
        self.classifier = None
        self.test_data = None
        self.assign_cleans()
        self.train_ai()

    def assign_cleans(self):
        print('Learning Positive Tweets')
        for tokens in twitter_samples.tokenized('positive_tweets.json'):
            self.clean_positive.append(remove_noise(tokens))
        print('Learning Negative Tweets')
        for tokens in twitter_samples.tokenized('negative_tweets.json'):
            self.clean_negative.append(remove_noise(tokens))

    def train_ai(self):
        all_pos_words = get_all_words(self.clean_positive)
        self.freq_dist_pos = FreqDist(all_pos_words)
        print('10 most Popular words: ')
        print(self.freq_dist_pos.most_common(10))
        positive_tokens_for_model = get_tweets_for_model(self.clean_positive)
        negative_tokens_for_model = get_tweets_for_model(self.clean_negative)
        positive_dataset = [(tweet_dict, "Positive")
                            for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, "Negative")
                            for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset
        random.shuffle(dataset)
        train_data = dataset[:7000]
        self.test_data = dataset[7000:]

        self.classifier = NaiveBayesClassifier.train(train_data)

    def accuracy_test(self):
        print('Performing Accuracy Test')
        print('Accuracy is:')
        print(classify.accuracy(self.classifier, self.test_data))
        print('---')
        print(self.classifier.show_most_informative_features(10))

# ... __END Sentiment Class


# .. Return each clean token mem safe with yield
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


# .. Shape for modeling
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def remove_noise(tweet_tokens):
    stop_words = stopwords.words('english')
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' 
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def run():
    print('Training AI...')
    sentiment = Sentiment()
    print('AI Trained')
    sentiment.accuracy_test()


if __name__ == '__main__':
    run()
