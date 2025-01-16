#logger configuration
import json
import logging
import time

from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaConsumer")


# consumer configuration
consumer = KafkaConsumer(
    "results_vote_per_candidate_topic",
    bootstrap_servers=["192.168.178.194:9092"],
    group_id=None,  # no consume group
    auto_offset_reset="earliest",
    enable_auto_commit=True,  # automatic message validation
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)



# function to print data in kafka votes_topic
def consume_data():
    # Attempt to consume messages with error handling.
    try:
        logger.info("Consumer started")
        try:

            while True:
                msg = consumer.poll(20)  # time in Second  to poll all message
                time.sleep(3)
                if len(msg) == 0:
                    print("wait a message")
                if msg is None:
                    logger.info("error during  poll message")
                    break

                else:
                    for message in msg.values():
                       results_vote_dict = message[0][6]
                       print(results_vote_dict["candidate_name"], results_vote_dict["candidate_picture"],results_vote_dict["vote"], sep=" ")


        except Exception as e:
            print ( "kafka error:" , e)

    except KeyboardInterrupt:
        logger.info("Consumption interrupted by user")

    finally:
        # Closing consumer
        logger.info("Closing consumer...")
        consumer.close()

if __name__ == "__main__":
    consume_data()