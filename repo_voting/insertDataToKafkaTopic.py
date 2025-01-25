from kafka import KafkaProducer
import json


# establish connection to Kafka
def Kafka_connection():
    return KafkaProducer(
        bootstrap_servers=['192.168.178.194:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )


# send data to kafka
def send_data_to_Kafka_topic(topic_name, data):
    try:
        producer = Kafka_connection()
        producer.send(topic_name, data)
        print(" send data ok")
    except Exception as e:
        print("error during data send:", e.__str__())
