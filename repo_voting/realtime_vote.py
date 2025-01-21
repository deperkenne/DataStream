import json
import random
import time
from datetime import datetime

import psycopg2
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, Row
from sparkstream.repo_voting import CreateAndIinsertDataToTable, insertdatatotables

if __name__ == "__main__":


        spark =(SparkSession.builder
                 .appName("votes")
                 .master("local[*]")  # L'IP de votre machine distante et le port du Spark Master
                 #.config("kafka.bootstrap.servers", "192.168.178.194:9092")  # Kafka service name from docker-compose
                 #.config("spark.sql.shuffle.partitions",3)
                 .config("spark.jars", "/opt/spark-apps/postgresql-42.7.3.jar")  # PostgreSQL driver
                 .config("spark.sql.adaptive.enabled", "false")  # Disable adaptive query execution
                 .getOrCreate()
                 )



        schema = StructType([
               StructField("voter_id", StringType(), nullable=False),
               StructField("candidate_id", StringType(), nullable=True),
               StructField("voting_time", TimestampType(), nullable=True),
               StructField("vote", IntegerType(), nullable=True)
               ])



        cur = None
        conn= None


        conn = psycopg2.connect(host="192.168.178.194",
             port="5432",
             dbname="db",
             user="root",
             password="root"   )
        print("connection to database success")
        cur = conn.cursor()


        # JDBC params connexion
        url = "jdbc:postgresql://192.168.178.194:5432/db"  # Exemple : jdbc:postgresql://localhost:5432/demo_db
        properties = {
            "user": "root",
            "password": "root",
            "driver": "org.postgresql.Driver"
        }
        table_name_candidates = "candidates"
        table_name_voters = "voters"
        table_name_votes = "votes"





        # Read data from table voters to dataframe
        def get_data_from_db(url,table_name,properties):
            try:
              return spark.read.jdbc(url=url, table=table_name, properties=properties)
            except Exception as e :
                print (e)
                return 1

            return 0

        # save data from db
        def save_data_from_db(df,url,table_name,properties):
            try:
                df.write.jdbc(url=url, table=table_name, properties=properties)
            except Exception as e:
                print(e)



        # establish connection to Kafka
        def Kafka_connection():
          return KafkaProducer(
            bootstrap_servers=['192.168.178.194:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )


        # send data to kafka
        def send_data_to_Kafka_topic(topic_name, **kwargs):
         try:
            producer = Kafka_connection()
            producer.send(topic_name, kwargs)
            print(" send data ok")
         except Exception as e:
            print("error during data send:", e.__str__())




        # insert data to votes table using spark db_connect (data storage)
        def insert_data_to_table_votes(voterId,candidatesID,votingTime,vote):
             data = [
                 Row(voter_id=voterId, candidate_id=candidatesID, voting_time=votingTime,vote=vote),
             ]

             df_votes = spark.createDataFrame(data,schema)
             save_data_from_db(df_votes,url,table_name_votes,properties)


        # starting vote

        def choice_candidate():
            vote = 1
            candidates_data= get_data_from_db(url,table_name_candidates,properties).collect()
            voters_data = get_data_from_db(url,table_name_voters,properties).collect()

            for voter in voters_data:
                 random_choice = random.choice(candidates_data)
                 candidate_name = random_choice["candidate_name"]
                 voting_time = datetime.now()
                 voting_time_str = voting_time.isoformat()

                 send_data_to_Kafka_topic("votes_topic",vote=vote,voter_id=voter["voter_id"],candidate_id= random_choice["candidate_id"],candidate_name=random_choice["candidate_name"],party_affiliation=random_choice["party_affiliation"],
                                         candidate_picture=random_choice["photo_url"],vote_time=voting_time_str) # kafka storage
                
                 insertdatatotables.save_data_to_table_vote(conn,cur,voter_id= voter["voter_id"],candidate_id=random_choice["candidate_id"],voting_time=voting_time,vote=vote)# db storage


                 time.sleep(5)

        
        # call function
        choice_candidate()
                
