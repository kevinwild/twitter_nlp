import settings
import requests
import json
from requests_oauthlib import OAuth1


class RequestApi:

    def __init__(self):
        self.insert_dict = []
        self.oauth = OAuth1(settings.CONSUMER_KEY,
                            settings.CONSUMER_SECRET,
                            settings.ACCESS_TOKEN,
                            settings.ACCESS_TOKEN_SECRET)

    def make_request(self, param):
        return requests.get(settings.CONFIG.get('search_url'), params=param, auth=self.oauth)

    def extract_data(self, tweet):
        if tweet['entities']['hashtags']:
            hashes = []
            for i in tweet['entities']['hashtags']:
                hashes.append(i["text"])
            hash_tags = hashes
        else:
            hash_tags = []

        tmp = {
            "userName": tweet['user']['name'],
            "userHandle": tweet['user']['screen_name'],
            "userFollowCnt": tweet['user']['followers_count'],
            "userFriendCnt": tweet['user']['friends_count'],
            "userLocation": tweet['user']['location'],
            "id": tweet['id'],
            "text": tweet['text'],
            "geo": tweet['place'],
            "lang": tweet['lang'],
            "retweetCount": tweet['retweet_count'],
            "favCount": tweet['favorite_count'],
            "hashTags": hash_tags
        }
        self.insert_dict.append(tmp)

    def write_file(self):
        save_path = settings.CONFIG.get('data_store_dir') + '/' + settings.CONFIG.get('raw_file_name')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.insert_dict, f, ensure_ascii=False)


def run():
    api_obj = RequestApi()
    for param in settings.CONFIG.get('query_params'):
        response = api_obj.make_request(param)
        for tweet in response.json()[u'statuses']:
            api_obj.extract_data(tweet)
        for i in range(3):  # 3 pages of results
            # next_page_url = search_url + response.json()['search_metadata']['next_results']
            for tweet in response.json()['statuses']:
                api_obj.extract_data(tweet)
    api_obj.write_file()


if __name__ == '__main__':
    run()
