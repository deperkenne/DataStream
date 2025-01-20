from unittest import mock

import pytest
import requests
import psycopg2
from unittest import mock
from .insertdatatotables import get_data



BASE_URL = 'https://randomuser.me/api/?nat=gb'
BASE_URL_NOT_EXIST = 'https://randomuser.'



@pytest.mark.parametrize("url,expected_list", [
    (BASE_URL,["male","male","female"] ),
    (BASE_URL, ["male", "male", "female"] ),
])
def test_return_correctly_list_of_candidates(url,expected_list):
    # given
    list_gender_expected = expected_list

    # when SUT
    list_candidate = get_data(url)
    list_genders = list(map(lambda candidate: candidate["gender"],list_candidate))

    # then
    assert set(list_gender_expected) == set(list_genders),"error not same containt"


# Mock pour requests.get
def mock_requests_get(*args, **kwargs):
    raise Exception("Simulated connection error")

@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_data_raises_exception_on_network_error(mock_get):
    """
    Test to verify that get_data handles network errors correctly.
    """
    BASE_URL = "https://invalid-url.com"

    with pytest.raises(Exception, match="Simulated connection error"):
        get_data(BASE_URL)

# Mock for get_data
def mock_get_data(*args, **kwargs):
    return set_up_mock_candidates()
# Mock for `get_data`
@mock.patch("get_data", return_value=mock_get_data)
def test_insert_candidates(mock_get_data):
    """
    Test to verify the insertion of candidates into the database.
    """
    # Connect to the test database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # Call the main function
        candidates_data = get_data(BASE_URL)
        i = 0  # Index for the parties

        for candidate in candidates_data:
            # Extract the candidate's unique identifier (UUID)
            uuid = candidate["login"]["uuid"]

            # Combine first and last names to construct the full name
            candidate_name = candidate["name"]["first"] + " " + candidate["name"]["last"]

            # Assign a party affiliation to the candidate
            party = PARTIES[i]

            # Placeholder text for the candidate's biography
            bio = "A brief bio of the candidate."

            # Placeholder text for the candidate's campaign platform
            campaign = "Key campaign promises or platform."

            # URL for the candidate's profile picture
            pict = candidate["picture"]["large"]

            # Increment the index to move to the next party
            i += 1

            # Execute the SQL INSERT query to add the candidate to the database
            cur.execute(
                """
                INSERT INTO candidates(candidate_id, candidate_name, party_affiliation, biography, campaign_platform, photo_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (uuid, candidate_name, party, bio, campaign, pict)
            )
            # Commit the transaction to save the changes
            conn.commit()

        # Verify that the data was inserted correctly
        cur.execute("SELECT * FROM candidates WHERE candidate_id = %s", ("1234-5678",))
        result = cur.fetchone()

        # Assert that the data exists in the database
        assert result is not None, "The data was not inserted into the database."
        # Assert that the candidate's name is correct
        assert result[1] == "John Doe", "The candidate's name is incorrect."
        # Assert that the party affiliation is correct
        assert result[2] == "Party A", "The party affiliation is incorrect."

        print("Test passed: Data was inserted correctly.")
    finally:
        # Clean up the database after the test
        cur.execute("DELETE FROM candidates WHERE candidate_id IN (%s, %s)", ("1234-5678", "8765-4321"))
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()





# configuration for db_test
DB_CONFIG = {
    "dbname": "test_db",
    "user": "test_user",
    "password": "test_password",
    "host": "localhost",
    "port": 5432
}

# Données de test
BASE_URL = "https://mock-api-url.com"

PARTIES = ["Party A", "Party B"]



def set_up_mock_candidates():
    return [
    {
        "login": {"uuid": "1234-5678"},
        "name": {"first": "John", "last": "Doe"},
        "picture": {"large": "https://example.com/picture.jpg"}
    },
    {
        "login": {"uuid": "8765-4321"},
        "name": {"first": "Jane", "last": "Smith"},
        "picture": {"large": "https://example.com/picture2.jpg"}
    },
]




















