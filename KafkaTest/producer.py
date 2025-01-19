
import logging
from time import sleep
import json
from kafka import KafkaProducer

# Dictionnaire à envoyer
data_dict = {
    "name": "kenne",
    "age": 35
}

def producer_init_and_send_data():
    # Configuration du logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("KafkaProducer")
    # Configuration du producteur
    producer = KafkaProducer(
        bootstrap_servers=["192.168.178.194:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),  # Sérialisation en JSON
    )

    send_data_to_topic(producer,logger,data_dict)



def send_data_to_topic(producer,logger,data):
    # Envoi du message au topic Kafka
    producer.send("event_topic3", data)
    producer.flush()

    # Log de confirmation avec des valeurs sérialisées
    logger.info("Successfully produced message with keys: %s, values: %s", list(data_dict.keys()),
                list(data_dict.values()))

    # Pause de 200ms entre les messages
    sleep(0.2)

    # Fermer le producteur
    producer.close()

producer_init_and_send_data()

