# from tweepy import API
# from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import json

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

        stream.filter(track=tags,locations = [-180,-90,180,90])

class TwitterListener(StreamListener):
    '''
    Class for tweets Listener
    '''

    def __init__(self, tweets_file):
        self.tweets_file = tweets_file

    def on_data(self,data):
        try:
            data = json.loads(data)
            if data['place']:
                print(data['place']['country_code'])
                with open(self.tweets_file,'a') as outfile:
                    json.dump(data['place'],outfile)
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self,status):
        if status == 420:
            #To terminate when rate limit exceeds
            return False
        print(status)

if __name__ == "__main__":

    tags = ['simplelife', 'simple','simpleliving','minimalism','simplicity','simplelife','livesimply','ilivesimply','simplylife',
            'degrowth','EcoMonday','Cleantech','Green','Environment','Ecofriendly','wildlife','nature','savetheplanet','climatechange',
            'reducewaste','recycle','reduce','reuse','reducereuserecycle','sustainablefuture','sustainability','zerowaste',
            'urbanfarming','declutter','countrylife','mothernature','villagelife','naturelife',
        ]
    tweets_file = "./../data/tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(tweets_file,tags)




