import requests

from .insertDataToKafkaTopic import send_data_to_Kafka_topic

BASE_URL = 'https://randomuser.me/api/?nat=gb'
PARTIES = ["Management Party", "Savior Party", "Tech Republic Party"]
cursor = None


def send_data_to_kafka(topic_data, **kwargs):
    send_data_to_Kafka_topic(topic_data, kwargs)


def get_data(base_url):
    candidate_id_list = {}  # Dictionary to track already fetched candidate IDs
    final_candidates = []  # List to store the final selection of candidates
    try:
        while True:
            # Send a GET request to the API
            response = requests.get(base_url)

            # Check if the API responded successfully
            if response.status_code == 200:
                # Parse the candidate data from the API response
                candidate_data = response.json()["results"][0]
                gender = candidate_data["gender"]

                # Construct a unique candidate ID from the "id" field
                candidate_id = "".join(candidate_data["id"].values())

                # Skip this candidate if the ID already exists in the list
                if candidate_id in candidate_id_list:
                    continue
                # Add the new candidate's ID to the dictionary
                candidate_id_list[candidate_id] = gender
                # Check if we already have 3 candidates in the final list
                if len(final_candidates) == 3:
                    break
                # Add a female candidate if there is no female yet in the list
                if (
                        gender == "female"
                        and
                        "female" not in [candidate["gender"]
                                         for candidate in final_candidates]
                ):
                    final_candidates.append(candidate_data)
                else:
                    # Ensure we only add male candidates
                    # if the list is not already complete
                    if (
                            len(final_candidates) == 2
                            and
                            "female" not in [candidate["gender"]
                                             for candidate in final_candidates]
                    ):
                        continue
                    else:
                        # Prevent adding more males if a female is already present
                        if gender == "female":
                            continue
                        final_candidates.append(candidate_data)
    except Exception as e:
        # Handle errors during API requests or other operations
        print(e.args)
        raise
    else:
        return final_candidates


def insert_data_to_db(conn, cur):
    """
    Insert candidate data into a database table called 'candidates'.

    Args:
        conn: Database connection object (psycopg2 connection).
        cur: Database cursor object (psycopg2 cursor).

    This function retrieves data using the `get_data()` function
    and inserts it into the database.
    Each candidate is assigned a unique ID (uuid), a name, a party affiliation,
    a biography, campaign platform information, and a photo URL.

    The database insertion is committed after each candidate is added.
    """
    i = 0
    candidates_data = get_data(BASE_URL)
    try:
        # Iterate over the candidate data retrieved from the API
        for candidate in candidates_data:
            # Extract unique identifier (uuid) for the candidate
            uuid = str(candidate["login"]["uuid"])
            # Construct the candidate's full name
            candidate_name = (candidate["name"]["first"] + " "
                              + candidate["name"]["last"]
                              )
            # Assign a party affiliation to the candidate
            party = PARTIES[i]
            # Placeholder text for the candidate's biography
            bio = "A brief bio of the candidate."
            # Placeholder text for the candidate's campaign platform
            campaign = "Key campaign promises or platform."
            # Extract the URL for the candidate's profile picture
            pict = candidate["picture"]["large"]
            # Increment the index to move to the next party in the PARTIES list
            i += 1
            # Execute the SQL INSERT query to add the candidate to the database
            cur.execute(
                """
                INSERT INTO candidates(candidate_id,candidate_name, party_affiliation,
                            biography, campaign_platform, photo_url)
                VALUES (%s, %s, %s, %s, %s,%s)
                """,
                (uuid, candidate_name, party, bio, campaign, pict)
            )

            # Commit the transaction to save the changes to the database
            conn.commit()
            print("insertion success")

    except Exception as e:
        print("error during insert data:", e.__str__())
    else:
        print("end insertion")
    finally:
        cur.close()
        conn.close()


def generate_voter_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        user_data = response.json()['results'][0]
        return {
            "voter_id": user_data['login']['uuid'],
            "voter_name": f"{user_data['name']['first']} {user_data['name']['last']}",
            "date_of_birth": user_data['dob']['date'],
            "gender": user_data['gender'],
            "nationality": user_data['nat'],
            "registration_number": user_data['login']['username'],
            "address": {
                "street": f"{user_data['location']['street']['number']} "
                          f"{user_data['location']['street']['name']}",
                "city": user_data['location']['city'],
                "state": user_data['location']['state'],
                "country": user_data['location']['country'],
                "postcode": user_data['location']['postcode']
            },
            "email": user_data['email'],
            "phone_number": user_data['phone'],
            "cell_number": user_data['cell'],
            "picture": user_data['picture']['large'],
            "registered_age": user_data['registered']['age']
        }
    else:
        return "Error fetching data"


def insert_voters_data_to_db(conn, cur):
    try:
        for _ in range(2):
            voter = generate_voter_data()
            cur.execute(
                """
                INSERT INTO voters (voter_id, voter_name,
                date_of_birth,
                gender, nationality,
                registration_number, address_street, address_city, address_state,
                address_country, address_postcode, email, phone_number, cell_number,
                picture, registered_age
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    voter["voter_id"],
                    voter["voter_name"],
                    voter["date_of_birth"],
                    voter["gender"],
                    voter["nationality"],
                    voter["registration_number"],
                    voter["address"]["street"],
                    voter["address"]["city"],
                    voter["address"]["state"],
                    voter["address"]["country"],
                    voter["address"]["postcode"],
                    voter["email"],
                    voter["phone_number"],
                    voter["cell_number"],
                    voter["picture"],
                    voter["registered_age"]
                )
            )
            conn.commit()
            print("Insertion successful")

    except Exception as e:
        print("Error during data insertion:", str(e))
    else:
        print("End of insertion process")


def insert_data_to_results_votes_table(cur, list_votes):
    try:
        for vote in list_votes:
            cur.execute(
                """
                INSERT INTO results_vote (
                candidate_id, candidate_name, party_affiliation,
                candidate_picture, total_votes
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    vote["candidate_id"],
                    vote["candidate_name"],
                    vote["party_affiliation"],
                    vote["candidate_picture"],
                    vote["total_votes"],
                )
            )
        print("Data successfully inserted into results_vote table.")
    except Exception as e:
        print("Error during data insertion:", str(e))


def save_data_to_table_vote(cur, **kwargs):
    cur.execute(
        """
        INSERT INTO results_vote(
        candidate_id, candidate_name,
        party_affiliation, candidate_picture, total_votes
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            kwargs["candidate_id"],
            kwargs["voter_id"],
            kwargs["voting_time"],
            kwargs["vote"]
        )
    )


def fetchall_candidates_table_data(cur):
    cur.execute("""SELECT * FROM candidates""")
    for candi in [candidate for candidate in cur.fetchall()]:
        print(candi)


def fetchall_voters_table_data(cur):
    cur.execute("""
             SELECT *  from voters
             LIMIT 10
             """)
    if len(list(cur.fetchall())) == 0:
        print("no data")
    for voter in [voter for voter in cur.fetchall()]:
        print(voter)


def fetchall_votes(cur):
    cur.execute("""
                SELECT *  from ecommerce
                LIMIT 10
            """)
    for vote in [vote for vote in cur.fetchall()]:
        print(vote)
