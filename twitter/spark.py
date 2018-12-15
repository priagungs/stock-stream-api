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

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# creat the Streaming Context from the above spark context with window size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("localhost",1234)

sampled_data = dataStream.transform(sampling_data)
tweets = sampled_data.filter(lambda input: filter_tweets(input))



# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()


