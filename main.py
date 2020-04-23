import request_api
import analyze_data

if __name__ == '__main__':

    #  .. Get tweets from twitter api and store locally in json file
    request_api.run()
    #  .. Read local json file containing tweets and generate report
    #analyze_data.run()
