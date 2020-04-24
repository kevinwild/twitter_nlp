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

`



  
