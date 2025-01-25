
import json
import logging
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaConsumer")
list_results_vote_to_save_to_db = []

# consumer configuration
consumer = KafkaConsumer(
                "results_vote_topic",
                bootstrap_servers=["192.168.178.194:9092"],
                group_id=None,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
           )


# function to print data in kafka votes_topic
def consume_data_from_kafka():
    list_candidate_vote_info = []
    # status = 0
    global list_results_vote_to_save_to_db
    # Attempt to consume messages with error handling.
    try:
        logger.info("Consumer started")
        try:
            while True:
                msg = consumer.poll(9000)
                if len(msg) == 0:
                    print("wait message")

                elif msg is None:
                    logger.info("error during  poll message")
                    break
                else:
                    for message in msg.values():
                        results_vote_dict = message[0][6]
                        print(results_vote_dict)
                        list_candidate_vote_info.append(results_vote_dict)
                    print("okay")
                    list_candidate_vote_info = []
        except Exception as e:
            print("kafka error:", e)
    except KeyboardInterrupt:
        logger.info("Consumption interrupted by user")
    finally:
        # Closing consumer
        logger.info("Closing consumer...")
        consumer.close()


if __name__ == "__main__":
    consume_data_from_kafka()
