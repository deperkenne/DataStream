import psycopg2
from insertdatatotables import fetchall_votes, fetchall_candidates_table_data, insert_data_to_db
from sparkstream.repo_voting.insertdatatotables import insert_voters_data_to_db

cur = None
conn= None

def connection_to_db():
    global conn
    global cur
    try:
      conn = psycopg2.connect(host="192.168.178.194",
            port="5432",
            dbname="my-db",
            user="kenne",
            password="kenne"   )
      print("connection to database success")
      cur = conn.cursor()


    except Exception as e:
        print("error :",e.__str__())



def create_table_candidates():
    global conn
    global cur
    try:
       cur.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                    candidate_id VARCHAR(255) PRIMARY KEY,
                    candidate_name VARCHAR(255),
                    party_affiliation VARCHAR(255),
                    biography TEXT,
                    campaign_platform TEXT,
                    photo_url TEXT
                    )
                """
            )

       conn.commit()
       print("table candidates create")
    except Exception as e:
       print(e)


def create_table_voters():
    global conn
    global cur
    try:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS voters (
                    voter_id VARCHAR(255) PRIMARY KEY,
                    voter_name VARCHAR(255),
                    date_of_birth VARCHAR(255),
                    gender VARCHAR(255),
                    nationality VARCHAR(255),
                    registration_number VARCHAR(255),
                    address_street VARCHAR(255),
                    address_city VARCHAR(255),
                    address_state VARCHAR(255),
                    address_country VARCHAR(255),
                    address_postcode VARCHAR(255),
                    email VARCHAR(255),
                    phone_number VARCHAR(255),
                    cell_number VARCHAR(255),
                    picture TEXT,
                    registered_age INTEGER
                )
                """

             )
        conn.commit()
        print("table voters create")
    except Exception as e:
        print(e)


def create_table_votes():
    global conn
    global cur
    try:

        cur.execute("""
              CREATE TABLE IF NOT EXISTS votes (
                  voter_id VARCHAR(255) UNIQUE,
                  candidate_id VARCHAR(255),
                  voting_time TIMESTAMP,
                  vote int DEFAULT 1,
                  PRIMARY KEY (voter_id, candidate_id)
              )
          """)
        conn.commit()
        print("table vote create")
    except Exception as e:
      print(e)


def create_table_results_vote():
  global conn
  global cur
  try:
     cur.execute("""
            CREATE TABLE IF NOT EXISTS results_vote (
                candidate_id VARCHAR(255) PRIMARY KEY,
                candidate_name VARCHAR(255),
                candidate_picture Text,
                party_affiliation Text,
                total_votes int   
                
            )
        """)
     conn.commit()
     print("table result create")
  except Exception as e:
      print(e)


def delete(cur):
    try:
        # Exécuter la commande DELETE pour supprimer toutes les lignes de la table votes
        cur.execute("DELETE FROM votes")

        # Commit si vous êtes dans une transaction
        cur.connection.commit()

        print("All records have been deleted from the votes table.")
    except Exception as e:
        # En cas d'erreur, rollback pour annuler toute modification
        cur.connection.rollback()
        print(f"An error occurred: {e}")



if __name__ == "__main__":
  connection_to_db()
  delete(cur)










