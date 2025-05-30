from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.functions import sum as _sum
from pyspark.sql.types import (StructType,
                               StructField,
                               StringType, IntegerType, TimestampType)

if __name__ == "__main__":

    try:
        spark = (
            SparkSession.builder
            .appName("votingApp")
            .master("local[*]")
            .config("spark.streaming.stopGracefullyOnShutdown", True)
            .config("spark.streaming.schemaInference", True)
            .config("spark.jars.packages",
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
            .config("spark.jars", "postgresql-42.7.3.jar")
            .config("spark.sql.adaptive.enabled", "false")
            .getOrCreate()
        )
    except Exception as e:
        print("error occur during :", e)

    else:
        spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
        candidates_schema = StructType([
            StructField("uuid", StringType(), False),  # VARCHAR(255) -> StringType()
            StructField("name", StringType(), True),  # VARCHAR(255) -> StringType()
            StructField("party", StringType(), True),  # VARCHAR(255) -> StringType()
            StructField("biog", StringType(), True),  # TEXT -> StringType()
            StructField("picture", StringType(), True)  # TEXT -> StringType()
        ])
        schema = StructType([
            StructField("voter_id", StringType(), False),
            StructField("candidate_name", StringType(), True),
            StructField("candidate_picture", StringType(), True),
            StructField("party_affiliation", StringType(), True),
            StructField("candidate_id", StringType(), nullable=True),
            StructField("voting_time", TimestampType(), nullable=True),
            StructField("vote", IntegerType(), nullable=True)
        ])

        # consume data from vote_topic in Kafka (data injection)
        # consume data from vote_topic in Kafka (data injection)
        def consume_data(
                format_name="kafka",
                host_port="192.168.178.194:9092",
                topic_name="candidates_topic"
        ):
            candidateDF = spark.readStream \
                .format(format_name) \
                .option("kafka.bootstrap.servers", host_port) \
                .option("subscribe", topic_name) \
                .option("startingOffsets", "earliest") \
                .load()

            return candidateDF.select(
                from_json(col("value").cast("string"), schema).alias("data")
            ).select("data.*")

        # casting type and watermarking
        votes_df = consume_data(topic_name="votes_topic")
        votes_df = votes_df.withColumn('vote', col('vote').cast(IntegerType()))
        enriched_votes_df = votes_df.withWatermark("voting_time", "1 minute")
        votes_per_candidate = enriched_votes_df.groupBy(
            "candidate_id", "candidate_name",
            "party_affiliation",
            "candidate_picture"
        ).agg(
            _sum("vote")
            .alias("total_votes")
        )

        # votes_per_candidate.show()
        def send_data_to_kafka():

            votes_per_candidate_to_kafka = votes_per_candidate.selectExpr(
                "to_json(struct(*)) as value"
            ) \
                .writeStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
                .option("topic", "results_vote_per_candidate_topic") \
                .outputMode("complete") \
                .option("checkpointLocation", "./checkpointdir1") \
                .start()
            votes_per_candidate_to_kafka.awaitTermination()

        # save data to results_votes_topic in kafka
        def send_data_stream_to_kafka_topic():
            try:
                even_df = consume_data(topic_name='votes_topic')
                even_df.createOrReplaceTempView("resultTest")
                writerDf = spark.sql(
                    """
                    SELECT
                    any_value(voter_id) as voter_id,
                    candidate_id,
                    any_value(voting_time) as voting_time,
                    any_value(vote)as vote,
                    count(*) as cnt FROM resultTest GROUP BY candidate_id
                    """
                )
                aggregaDf = writerDf.selectExpr("to_json(struct(*)) AS value")
                query = aggregaDf.writeStream \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
                    .option("topic", "results_votes_topic") \
                    .outputMode("update") \
                    .format("console") \
                    .option("checkpointLocation", "./checpoint_dir_kafka") \
                    .start()
                query.awaitTermination()
                print("send data success")
            except Exception as e:
                print("error:", e)

        if __name__ == "__main__":
            send_data_to_kafka()
