from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests
import json

def sampling_data(rdd):
    return rdd.sample(False, 0.5, 10)

def filter_tweets(payload):
    json_payload = json.loads(payload)
    if 'text' in json_payload:
        return True
    return False

def filter_tweets_by_user_verified(tweet):
		json_tweet = json.loads(tweet)
		return json_tweet["user"]["verified"]

def function():
	pass
def iterate_function(rdd, **kwargs):
	rdd.foreach(lambda record: kwargs["verified"].add(1) \
    if json.loads(record)["user"]["verified"] else kwargs["not_verified"].add(1))

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp").setMaster('local[1]')
# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# creat the Streaming Context from the above spark context with window size 1 seconds
ssc = StreamingContext(sc, 1)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("localhost",1234)

sampled_data = dataStream.transform(sampling_data)

tweets = sampled_data.filter(lambda input: filter_tweets(input))
tweets_by_user_verified = tweets.filter(lambda input: filter_tweets_by_user_verified(input))

verified_tweets_count = sc.accumulator(0)
not_verified_tweets_count = sc.accumulator(0)

tweets.foreachRDD(lambda rdd: iterate_function(rdd, verified=verified_tweets_count, not_verified=not_verified_tweets_count))

# print(verified_tweets_count.value)
# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()

print(verified_tweets_count.value)


