import settings
import requests
import json
from requests_oauthlib import OAuth1


# === ====== ===
# ... Config
search_url = "https://api.twitter.com/1.1/search/tweets.json"
parametersArr = [
    {"q": ["nike"], "count": 1000000, "lang": "en"},
    {"q": ["burgers"], "count": 1000000, "lang": "en"}

]

# ... Create oAuth obj
oauth = OAuth1(settings.CONSUMER_KEY,
               settings.CONSUMER_SECRET,
               settings.ACCESS_TOKEN,
               settings.ACCESS_TOKEN_SECRET)
# .. Global Vars
insertDic = []


# === ====== ===


def extractData(tweet):
    if tweet['entities']['hashtags']:
        hashes = []
        for i in tweet['entities']['hashtags']:
            hashes.append(i["text"])
        hashTags = hashes
    else:
        hashTags = []

    tmp = {
        "userName": str(tweet['user']['name']),
        "userHandle": str(tweet['user']['screen_name']),
        "userFollowCnt": str(tweet['user']['followers_count']),
        "userFriendCnt": str(tweet['user']['friends_count']),
        "userLocation": str(tweet['user']['location']),
        "id": str(tweet['id']),
        "text": str(tweet['text']),
        "geo": str(tweet['place']),
        "lang": str(tweet['lang']),
        "retweetCount": str(tweet['retweet_count']),
        "favCount": str(tweet['favorite_count']),
        "hashTags": str(tweet['favorite_count'])
    }
    insertDic.append(tmp)


def writeToFile():
    with open('test.json', 'w') as f:
        json.dump(insertDic, f)


def makeRequest(params):
    return requests.get(search_url, params=params, auth=oauth)


def run():
    for param in parametersArr:
        response = makeRequest(param)
        for tweet in response.json()[u'statuses']:
            extractData(tweet)
        for i in range(3):  # 3 pages of results
            # next_page_url = search_url + response.json()['search_metadata']['next_results']
            for tweet in response.json()['statuses']:
                extractData(tweet)
    writeToFile()


if __name__ == '__main__':
    run()
