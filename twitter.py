import os
import json
import socket
import tweepy

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from signal import signal, SIGPIPE, SIG_DFL

# Stop program if sigpipe detected
signal(SIGPIPE, SIG_DFL)

CONSUMER_KEY = "aizws0k5M5ynyItQ8rG6RZsRi"
CONSUMER_SECRET = "i6BueqJFS0kQN4RLZwLwak1mz1vj1ddQyzQ0IYP9aTnJmAkZJP"
ACCESS_TOKEN = "75783613-gO9I5WKQ8vTV2zlginSCSKphYlGrS9zwz26n3xHmk"
ACCESS_SECRET = "Kp6d0YrW6Qt8ZW8BraRw96j4zBVURpfrV3VLLMZbuCO9h"

class TweetStream(StreamListener):
    def __init__(self, sparkConnection):
        super().__init__()
        self.sparkConnection = sparkConnection

    def on_data(self, tweet):
        self.sparkConnection.send(tweet.replace(r'\n','').encode())

    def on_error(self, status):
        if status == 420:
            print("Stream Disconnected")
        return False

def sendTwitterData(sparkConnection):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth = api.auth, listener=TweetStream(sparkConnection))
    stream.sample()

if __name__ == "__main__":
    TCP_IP = "localhost"
    TCP_PORT = 1234
    sparkConnection = None
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)
    print("TCP-IP socket waiting for socket connection")
    sparkConnection, address = s.accept()
    print("TCP-IP socket connnected...")

    sendTwitterData(sparkConnection)