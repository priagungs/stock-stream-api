import os
import json
import socket
import tweepy

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from signal import signal, SIGPIPE, SIG_DFL

CONSUMER_KEY = "aizws0k5M5ynyItQ8rG6RZsRi"
CONSUMER_SECRET = "i6BueqJFS0kQN4RLZwLwak1mz1vj1ddQyzQ0IYP9aTnJmAkZJP"
ACCESS_TOKEN = "75783613-gO9I5WKQ8vTV2zlginSCSKphYlGrS9zwz26n3xHmk"
ACCESS_SECRET = "Kp6d0YrW6Qt8ZW8BraRw96j4zBVURpfrV3VLLMZbuCO9h"

class TweetStream(StreamListener):
    def __init__(self):
        super().__init__()

    def on_data(self, tweet):
        print(tweet.replace(r'\n',''))

    def on_error(self, status):
        if status == 420:
            print("Stream Disconnected")
        return False

def sendTwitterData():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth = api.auth, listener=TweetStream())
    stream.sample()

if __name__ == "__main__":
    sendTwitterData()