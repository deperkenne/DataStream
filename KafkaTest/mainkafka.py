from kafka import KafkaProducer
import logging
import random
import time

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaProducer")

# Configuration du producteur
producer = KafkaProducer(
    bootstrap_servers=["192.168.178.194:9092"],
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: str(v).encode("utf-8"),
)

# Liste des capteurs
sensors = ["sensor_1", "sensor_2", "sensor_3"]

try:
    while True:
        # Génération aléatoire de données
        key = random.choice(sensors)  # Clé (nom du capteur)
        value = random.randint(-20, 180)  # Valeur aléatoire (température)

        # Envoi du message au topic Kafka
        producer.send("RawTempReadings", key=key, value=value)
        producer.flush()

        # Log de confirmation
        logger.info(f"Successfully produced message from sensor {key} with value {value}")
        time.sleep(0.2)  # Pause de 200ms entre les messages

except KeyboardInterrupt:
    logger.info("Shutting down producer...")
finally:
    producer.close()
