import requests
from requests.auth import HTTPBasicAuth

import tweepy
from kafka import KafkaProducer
import json
# Vos informations d'authentification Twitter
bearer_token = "AAAAAAAAAAAAAAAAAAAAAENBxgEAAAAAaUBO7KUi%2BkcVpyldsLHIsPR9DLc%3DSXre9YmfJQxWnnFhUeD7e20UEcvf44soiy5uDm5l5LpF9kebYq"
comsumer_key = "BENAN8McLPEE4TYa5XI7cSSOf"
comsumer_key_secret = "i3ztMoRPnLaFEskuo02FY8QB7C8jLDNjXUtYu780VjOnxvet57"
# Créer un producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=['192.168.178.182:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)



# Classe pour écouter les tweets en temps réel
class TweetListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_data = {
            'user': tweet.author_id,  # Note : 'author_id' est l'ID de l'utilisateur, pas le nom d'écran
            'tweet': tweet.text,
            'created_at': str(tweet.created_at) if tweet.created_at else "N/A"
        }
        # Envoi du tweet dans Kafka
        producer.send('event_topic', value=tweet_data)
        print(f"Tweet envoyé à Kafka: {tweet_data}")

    def on_errors(self, errors):
        print(f"Erreur : {errors}")

    def on_connection_error(self):
        print("Erreur de connexion.")
        self.disconnect()

# Initialisation du flux pour suivre les tweets en temps réel
stream_listener = TweetListener(bearer_token)

# Ajouter des règles pour filtrer les tweets
try:
    stream_listener.add_rules(tweepy.StreamRule("conference"))  # Mots-clés ici
    print("Règle ajoutée avec succès !")
except tweepy.TweepyException as e:
    print(f"Erreur lors de l'ajout des règles : {e}")
    exit()

# Commencer le streaming des tweets
try:
    print("Démarrage du streaming...")
    stream_listener.filter()
except KeyboardInterrupt:
    print("Streaming arrêté.")
    exit()
except Exception as e:
    print(f"Erreur pendant le streaming : {e}")


