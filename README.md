## Twitter Python NLP

**Installation**

 1. **Clone the repo**: `git clone https://github.com/kevinwild/twitter_nlp`

 2. **Copy sample.env from root to .env and set your twitter API keys**

 3. **Install dependencies**: 
  `pip install requests_oauthlib nltk  emoji`

  4. **Configure config.json**
	  - **data_store_dir** = folder for writing files
	   - **raw_file_name** = file name for raw data from API 
	   - **report_file_name** = file name for final report
	   - **confidence_level** = the level of  probability confidence that the AI has chosen the right tone for the tweet. If the tweets confidence number is lower then this number it will not be considered a valid tweet for the sentiment analysis
	   - **tweet_save_limit** = the confidence level of tweets that should be added to the final report. 
	   - **top_word_limit** = the number of most frequent words used throughout the data set.
	   - **search_url** = the main search URL,  other URLs must have similar return json shape.
	   - **query_params** = list of query parameters used for each API request. [Full list found here](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets) 
5. **Run the entire program or only a section. The program overwrites their output file and `analyze_data.py` always has to be ran after `request_api.py`**
	- **run entire program**: `python main.py`
	or
	- **generate raw data**: `python request_api.py`
	- 	**generate report**: `python analyze_data.py`

---
**Report Generates the following data**:
- **total_tweets** = number of total tweets
- **positive_count** = number of tweets that are considered positive and within the confidence threshold
- 	**negative_count** = number of tweets that are considered negative and within the confidence threshold
-	**total_certain_positive** = number of tweets that are considered positive and within the tweet_save_limit threshold
-	**total_certain_negative** = number of tweets that are considered negative and within the tweet_save_limit threshold
-	**positive_tweets** = An array of objects that show positive tweets and the probability it is considered positive
- **negative_tweets** = An array of objects that show negative tweets and the probability it is considered negative
-	**top_N_words** = multi-dimensional array with the first index being the word and the second index showing the usage count
-	**emoji_count** = multi-dimensional array with the first index being the emoji and the second index showing the usage count
-	**user_locations** = multi-dimensional array with the first index being the location name and the second index showing the amount of times that location was used in a tweet

`



  
