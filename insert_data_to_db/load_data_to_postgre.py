

import random

import psycopg2
import requests
import simplejson as json
from confluent_kafka import SerializingProducer

BASE_URL = 'http://localhost:5003/records'


def generate_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        user_data = response.json()
        return {
            "user_id": user_data[0],
            "user_sentiment": user_data[1],
        }
    else:
        return "Error fetching data"

print(generate_data())

def create_tables(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Christmas_sentiment (
            id VARCHAR(255) PRIMARY KEY,
            nature VARCHAR(255),
        )
    """)

    conn.commit()


def insert_data(conn, cur, data):
  for record in data:

     cur.execute("""
                        INSERT INTO voters (id, nature)
                        VALUES (%s, %s)
                        """,
                (record["id"],record['nature'])

                )
  conn.commit()


if __name__ == "__main__":
    conn = psycopg2.connect("host=192.168.178.194:5432 dbname=airflow_db user=kenne password=Kenne1989")
    cur = conn.cursor()
    create_tables(conn, cur)

    # get candidates from db
    cur.execute("""
        SELECT * FROM 
    """)
    candidates = cur.fetchall()
    print(candidates)

    if len(candidates) == 0:
        for i in range(3):
            candidate = generate_candidate_data(i, 3)
            print(candidate)
            cur.execute("""
                        INSERT INTO candidates (candidate_id, candidate_name, party_affiliation, biography, campaign_platform, photo_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                candidate['candidate_id'], candidate['candidate_name'], candidate['party_affiliation'], candidate['biography'],
                candidate['campaign_platform'], candidate['photo_url']))
            conn.commit()





