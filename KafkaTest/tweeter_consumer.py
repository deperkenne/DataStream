from confluent_kafka import Consumer, KafkaError, KafkaException

import logging
import json
from kafka import KafkaConsumer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaConsumer")
list_of_sentiment = []
# consumer configuration
consumer = KafkaConsumer(
    "event_topic",
    bootstrap_servers=["192.168.178.194:9092"],
    group_id=None,  # no consume group
    auto_offset_reset="earliest",
    enable_auto_commit=True,  # automatic message validation
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)



def consume_data():
    record_list =[]
    # Attempt to consume messages with error handling.
    try:
        logger.info("Consumer started")
        try:
            msg = consumer.poll(2000) # time in Second  to poll all message
            if len(msg)== 0:
                print("no message in topic event_topic")
                exit()
            if msg is None:
                print("error during  poll message")
            else:
                for message in msg.values():
                   for record in message:
                       record_list.append(record[6])
                       print(record[6])
            return record_list

        except Exception as e:
            print ( "kafka error:" , e)

    except KeyboardInterrupt:
        logger.info("Consumption interrupted by user")

    finally:
        # Closing consumer
        logger.info("Closing consumer...")
        consumer.close()


def add_record(**kwargs):
  dict_tweet = {}
  global  list_of_sentiment
  for keys,values in kwargs.items():
      dict_tweet.setdefault(keys,values)
  list_of_sentiment.append(dict_tweet)


def sentiments_analyse():
    global list_of_sentiment
    list_record = consume_data()
    sentiments_description = ["positive","negative","neutral"]
    # text of tweet filter
    if list_record is None:
        return []
    for record in list_record:
        tweet = record["text"]
        # Créer un analyseur VADER
        analyzer = SentimentIntensityAnalyzer()
        # Analyser le sentiment
        sentiment_score = analyzer.polarity_scores(tweet)
        compound = sentiment_score['compound']
        if compound > 0.05:
            add_record(id=record["id"], nature=sentiments_description[0])
        elif compound < -0.05:
            add_record(id=record["id"],nature=sentiments_description[1])
        else:
          add_record(id=record["id"],nature=sentiments_description[2])
    return list_of_sentiment

print(sentiments_analyse())

