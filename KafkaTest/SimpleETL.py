from confluent_kafka import Consumer, Producer, KafkaException
import json

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': '192.168.178.194:9092',
    'group.id': 'weather.filter.group',
    'auto.offset.reset': 'earliest',
}

# Configuration du producteur Kafka
producer_config = {
    'bootstrap.servers': '192.168.178.194:9092',
}

# Créez une instance du consommateur Kafka
consumer = Consumer(consumer_config)

# Créez une instance du producteur Kafka
producer = Producer(producer_config)

# Abonnez-vous au topic 'RawTempReadings'
consumer.subscribe(['RawTempReadings'])


# Fonction pour traiter et filtrer les messages
def process_message(msg):
    try:
        # Décoder la clé et la valeur du message
        key = msg.key().decode('utf-8') if msg.key() else None
        value = int(msg.value().decode('utf-8'))

        # Appliquer une règle de validation
        if 10 < value < 130:
            print(f"Validating and sending {key}: {value}")
            # Produire vers le topic 'ValidatedTempReadings' c'ad les message filtre sont envoyer vers un autre topic dans le broker-1
            producer.produce('ValidatedTempReadings', key=key, value=str(value))
            producer.flush()
        else:
            print(f"Invalid reading {key}: {value} (out of range)")

    except Exception as e:
        print(f"Error processing message: {e}")


def send_message_to_topic():
    print("Starting simple ETL")
    try:
        while True:
            # Polling pour lire les messages  ecoute de tous les message du topic RawTempReadings
            msg = consumer.poll(timeout=1.0)  # Timeout de 1 seconde
            if msg is None:
                # Aucune donnée disponible
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Processer chaque message
                process_message(msg)

    except KeyboardInterrupt:
        pass
    finally:
        # Fermer le consommateur et le producteur proprement
        consumer.close()
        producer.close()

    print("ETL process finished.")
