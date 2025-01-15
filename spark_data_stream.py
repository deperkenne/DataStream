from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.functions import sum as _sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType



if __name__ == "__main__":
     
    try:
        spark = (SparkSession.builder
                 .appName("Sentiment")
                 .master("local[*]")  # L'IP de votre machine distante et le port du Spark Master
                 #.config("kafka.bootstrap.servers", "192.168.178.194:9092")  # Kafka service name from docker-compose
                 #.config("spark.sql.shuffle.partitions",3)
                 .config("spark.streaming.stopGracefullyOnShutdown",True)
                 .config("spark.streaming.schemaInference",True)
                 .config("spark.jars.packages",
                  "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")  # Spark-Kafka integration
                 #.config("spark.jars", "java-diver/postgresql-42.7.3.jar")  # PostgreSQL driver
                 .config("spark.jars", "postgresql-42.7.3.jar")

                 .config("spark.sql.adaptive.enabled", "false")  # Disable adaptive query execution
                 .getOrCreate()
                 )
    except Exception as e:
        print("error occur during :",e)

    else:
        spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")


        # Définir le schema Spark
        candidates_schema = StructType([
                  StructField("uuid", StringType(), False),       # VARCHAR(255) -> StringType()
                  StructField("name", StringType(), True),       # VARCHAR(255) -> StringType()
                  StructField("party", StringType(), True),    # VARCHAR(255) -> StringType()
                  StructField("biog", StringType(), True),            # TEXT -> StringType()
                  StructField("picture", StringType(), True)             # TEXT -> StringType()
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
        def consume_data(format_name="kafka",host_port="192.168.178.194:9092",topic_name="candidates_topic"):
            candidateDF= spark.readStream \
            .format(format_name) \
            .option("kafka.bootstrap.servers", host_port) \
            .option("subscribe", topic_name) \
            .option("startingOffsets", "earliest") \
            .load()
            return candidateDF.select(from_json(col("value").cast("string"),schema).alias("data")) \
                .select("data.*")



        # Data preprocessing: type casting and watermarking
        votes_df = consume_data(topic_name="votes_topic")
        votes_df = votes_df.withColumn('vote', col('vote').cast(IntegerType()))
        enriched_votes_df = votes_df.withWatermark("voting_time", "1 minute")

        # Aggregate votes per candidate
        votes_per_candidate = enriched_votes_df.groupBy("candidate_id", "candidate_name", "party_affiliation",
                                                            "candidate_picture").agg(_sum("vote").alias("total_votes"))
        #votes_per_candidate.show()

        

       



        
        def send_data_to_kafka():

            votes_per_candidate_to_kafka = votes_per_candidate.selectExpr("to_json(struct(*)) as value") \
                                       .writeStream \
                                       .format("kafka") \
                                       .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
                                       .option("topic","results_vote_per_candidate_topic") \
                                       .outputMode("complete") \
                                       .option("checkpointLocation" , "./checkpointdir1") \
                                       .start()


            votes_per_candidate_to_kafka.awaitTermination()






        # save data to results_votes_topic in kafka
        def send_data_stream_to_kafka_topic():

          try:
            even_df = consume_data(topic_name = 'votes_topic')
            even_df.createOrReplaceTempView("resultTest")
            writerDf = spark.sql(""" SELECT
                                      any_value(voter_id) as voter_id, 
                                      candidate_id, 
                                      any_value(voting_time) as voting_time,
                                      any_value(vote)as vote,count(*) as cnt FROM resultTest GROUP BY candidate_id """)
            aggregaDf = writerDf.selectExpr("to_json(struct(*)) AS value")

        
            query = aggregaDf.writeStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
                .option("topic", "results_votes_topic") \
                .outputMode("update") \
                .format("console") \
                .option("checkpointLocation","./checpoint_dir_kafka") \
                .start()
            query.awaitTermination()

            print("send data success")
          except Exception as e:
            print("error:",e)


    


        # show data consume
        def show_data_consume():
            castDf = consume_data()

            query =canditDf\
                  .writeStream\
                  .outputMode("complete")\
                  .format("console") \
                  .start()
            query.awaitTermination()
        


        if __name__ == "__main__":
             # send_data_stream_to_kafka_topic()
             send_data_to_kafka()

        """

        # load data from db
        def load_data_from_db(df,url,table_name,properties):
            df.write.jdbc(url=url, table=table_name, properties=properties):wq



        # insert data to votes table using spark db_connect (data storage)
        def insert_data_to_table_votes_and_topic(voterId,candidatesID,votingTime):
             data = [
                 Row(voter_id=voterId, candidate_id=candidatesID, voting_time=votingTime),
             ]
             df_votes = spark.createDataFrame(data,schema)
             load_data_from_db(df_votes,url,table_name_votes,properties)


        #send_data_to_votes_topic(df)

        #spark.sparkContext.setLogLevel("DEBUG")
        # Define schemas for Kafka topics
        event_schema = StructType([
            StructField("name", StringType(), True),
        ])


         # starting vote
        def choice_candidate():
         vote = 0


         try:
            candidates_data= get_data_from_db(url,table_name_candidates,properties).collect()
            voters_data = get_data_from_db(url,table_name_voters,properties).collect()

            for voter in voters_data:
                random_choice = random.choice(candidates_data)
                candidate_name = random_choice["candidate_name"]
                date_example = datetime.now()
                year = date_example.year
                month = date_example.month
                day = date_example.day
                hour = date_example.hour
                minute = date_example.minute

                voting_time = datetime(year,month,day,hour,minute)
                send_data_to_Kafka_topic("votes_topic",voter_id= voter["voter_id"],candidate_id= random_choice["candidate_id"                ],vote_time=voting_time)
                insert_data_to_table_votes_and_topic(voter["voter_id"],random_choice["candidate_id"],voting_time)
                vote +=1


         except Exception as e :
            print("error:",e)


        if __name__ == "__main__":
           choice_candidate()       

        
    

        # Read data from Kafka 'event_topic' and process it
        event_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
            .option("subscribe", "event_topic2") \
            .option("startingOffsets", "earliest") \
            .load()
        #castDf = event_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        
        castDf = event_df.select(from_json(col("value").cast("string"), event_schema).alias("data")) \
          .select("data.*")
        castDf.printSchema()
        


        query = castDf\
            .writeStream\
            .outputMode("append")\
            .format("console") \
            .start()


        query.awaitTermination()

        ds = castDf.selectExpr("to_json(struct(*)) AS value") \
            .writeStream \
            .outputMode("append") \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "192.168.178.194:9092") \
            
.option("topic", "event_test") \
            .option("checkpointLocation","C:/tmp/dtn2/kafka_checkpoint")\
            .start()
        ds.awaitTermination()
        """
        
