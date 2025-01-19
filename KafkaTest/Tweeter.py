import time

import tweepy
from kafka import KafkaProducer
import json
from tweetersecret import *

cursor = None


# kafka configuration
producer = KafkaProducer(
    bootstrap_servers=['192.168.178.194:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


# tweeter client Authentication
def clientAuthentication():
    auth = tweepy.OAuth1UserHandler(client_Id, client_secret, access_token, access_token_secret)
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        print("authentication success!")
    except Exception as e:
        print("authentication error:", e)
        exit()
    return client


# send tweeter message to broker topic
def send_tweet_to_topic():
    client = clientAuthentication()


    try:
        # search a lastly tweets
        response = client.search_recent_tweets(query="Christmas")
        print(response)

        # verify if the tweet exist
        if response.data:
            for tweet in response.data:
                tweet_data = {
                    "id": tweet.id,
                    "text": tweet.text
                }
                print("Tweet find :", tweet_data)

                producer.send("event_topic", tweet_data)
                print("tweet send with success !")
        else:
            print("no tweet exist with this request.")

    except Exception as e:
        print("error occur during the finding the tweets:", e)



send_tweet_to_topic()


"""
# Classe pour écouter les tweets en temps réel
class TweetListener(tweepy.StreamingClient):
    def on_status(self, status):
        tweet_data = {
            'user': status.user.screen_name,
            'tweet': status.text,
            'created_at': str(status.created_at)
        }
        # Envoi du tweet dans Kafka
        producer.send('events_topic', value=tweet_data)
        print(f"Tweet envoyé à Kafka: {tweet_data}")

# Initialisation du flux pour suivre les tweets en temps réel
stream_listener = TweetListener(bearer_token)
#stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Filtrer les tweets par mots-clés
#stream.filter(track=['#conference', '#sport', '#concert', '#gathering'])
# Filtrer les tweets en fonction des mots-clés (exemple: "conference")
stream_listener.add_rules(tweepy.StreamRule("conference"))

# Commencer le stream
stream_listener.filter()





# Classe pour gérer le streaming des tweets
class TweetStreamListener(tweepy.StreamingClient):
    def on_connect(self):
        print("Connecté au streaming Twitter API v2.")

    def on_tweet(self, tweet):
        print("Nouveau tweet :", tweet.text)
        producer.send("event_topic", {"id": tweet.id, "text": tweet.text})


# Initialiser et démarrer le streaming
try:
    stream_listener = TweetStreamListener(bearer_token)
    stream = tweepy.Stream(auth=tweepy.api.auth, listener=stream_listener)
    stream.add_rules(tweepy.StreamRule("sport"))  # Filtre par mot-clé
    stream.filter()
except Exception as e:
    print("Erreur du streaming :", e)

"""



