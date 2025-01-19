
from confluent_kafka import Consumer, Producer, KafkaException

from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor
i

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'weather.filter.group',
    'auto.offset.reset': 'earliest',
}


class ConsoClasse:
    ListConso = []
    @staticmethod
    def createConso(conso:Consumer):
        ConsoClasse.ListConso.append(conso)
    @staticmethod
    def consoSubmit(lis_topic:list):
        i = -1
        for conso in ConsoClasse.ListConso:
            topic = lis_topic[i+1]
            conso.subscribe([topic])



    # Fonction pour consommer les messages
    @staticmethod
    def consume_messages(thread_id, topic, bootstrap_servers):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id='consumer-group-1',  # Tous les consommateurs doivent être dans le même groupe
            auto_offset_reset='earliest',  # Commencer à lire depuis le début du topic
            enable_auto_commit=True
        )

        print(f"Thread {thread_id} started consuming from topic '{topic}'...")

        # consummer est object iterable qui retourne un consummerrecord qui contient les attribut key,value,partition ,offset
        # message ou consummerreccord
        print(list(consumer)[0])

        for message in consumer:
            print(
                f"Thread {thread_id} received: key={message.key}, partition={message.partition},offset={message.offset}")
            # Vous pouvez ajouter ici des traitements spécifiques

     # Créer plusieurs threads consommateurs
    @staticmethod
    def start_consumers(topic, bootstrap_servers, num_consumers=3):
        with ThreadPoolExecutor(max_workers=num_consumers) as executor:
            for thread_id in range(num_consumers):
                executor.submit(ConsoClasse.consume_messages, thread_id, topic, bootstrap_servers)



ConsoClasse.start_consumers('event_topic','127.0.0.1:9092')