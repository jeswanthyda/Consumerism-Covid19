
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import json
import time
from collections import defaultdict
from datetime import datetime
from pymongo import MongoClient

import twitter_credentials

class TwitterStreamer():
    '''
    Class for Streaming and Processing live tweets
    '''
    def __init__(self):
        pass

    def stream_tweets(self,tweets_file,tags):
        # Handle auth and connect to Twitter Streaming API
        listener = TwitterListener(tweets_file)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_SECRET)
        stream = Stream(auth, listener)
        stream.filter(track=tags)
        self.count = listener.count

class TwitterListener(StreamListener):
    '''
    Class for tweets Listener
    '''

    def __init__(self, tweets_file):
        self.tweets_file = tweets_file
        self.db = MongoClient("mongodb+srv://dbuser:TCS-Consumerism@cluster0-tchxh.mongodb.net/<dbname>?retryWrites=true&w=majority").ConsumerismInsights
        prev_values = self.db.twitter.find_one({})
        self.count_data = defaultdict(int)
        self.count_data.update(prev_values)
        self.past_time = datetime.now()

    def pushToMongo(self):
        world_count = dict(self.count_data)
        world_count["documentID"] = "world_count"
        query = {"documentID": "world_count"}
        self.db.twitter.update_one(query, {"$set":world_count}, upsert=True)
        print('Updated MongoDB at', str(datetime.now()))

    def on_data(self,data):
        try:
            data = json.loads(data)
            if data['place'] and data['place']['country_code'] != '':
                self.count_data[data['place']['country_code']] = self.count_data[data['place']['country_code']]+1

            if int((datetime.now()-self.past_time).seconds) >= 60:
                self.pushToMongo()
                self.past_time = datetime.now()
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self,status):
        if status == 420:
            #To pause when rate limit exceeds
            print('420 Error: Sleeping for 60 seconds')
            time.sleep(60)
        print(status)
        return True

if __name__ == "__main__":

    tags = ['simplelife', 'simple','simpleliving','minimalism','simplicity','simplelife','livesimply','ilivesimply','simplylife',
            'degrowth','EcoMonday','Cleantech','Green','Environment','Ecofriendly','wildlife','nature','savetheplanet','climatechange',
            'reducewaste','recycle','reduce','reuse','reducereuserecycle','sustainablefuture','sustainability','zerowaste',
            'urbanfarming','declutter','countrylife','mothernature','villagelife','naturelife',
        ]
    tweets_file = "./../data/tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(tweets_file,tags)

