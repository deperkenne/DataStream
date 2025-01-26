from unittest import mock
from unittest.mock import MagicMock
import pytest
from .CreateAndIinsertDataToTable import create_table_candidates
from .insertdatatotables import get_data, fetchall_candidates_table_data

BASE_URL = 'https://randomuser.me/api/?nat=gb'
BASE_URL_NOT_EXIST = 'https://randomuser.'


@pytest.mark.parametrize(
    "url,expected_list", [
        (BASE_URL, ["male", "male", "female"]),
        (BASE_URL, ["male", "male", "female"]),
    ]
)
def test_return_correctly_list_of_candidates(url, expected_list):
    # given
    list_gender_expected = expected_list

    # when SUT
    list_candidate = get_data(url)
    list_genders = list(
        map(lambda candidate: candidate["gender"], list_candidate)
    )

    # then
    assert set(list_gender_expected) == set(list_genders), "error not same containt"


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


def test_load_data_correctly_from_db():
    # given

    mock_cursor = MagicMock()

    # when
    fetchall_candidates_table_data(mock_cursor)

    # then
    mock_cursor.execute.assert_called_once_with("""SELECT * FROM candidates""")
    mock_cursor.fetchall.assert_called_once()


voter_id_1 = 140
voter_id_2 = voter_id_1 + 1


def setUpMockVoterData():
    global voter_id_1
    voter_id_1 += 1
    return {
        "voter_id": voter_id_1,
        "voter_name": "John Doe",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "nationality": "US",
        "registration_number": "123456",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "postcode": "10001",
        },
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "cell_number": "0987654321",
        "picture": "http://example.com/picture.jpg",
        "registered_age": 30,
    }


'''
# Patch generate_voter_data
@mock.patch(
      "sparkstream.repo_voting.insertdatatotables.generate_voter_data",
      side_effect=setUpMockVoterData
)
def test_insert_voters_data_to_db(mock_generate_voter_data):
    global voter_id_1
    global voter_id_2
    # given

    mock_conn = psycopg2.connect(host="192.168.178.194",
            port="5432",
            dbname="my-db",
            user="kenne",
            password="kenne" )
    mock_cursor = mock_conn.cursor()



    # when
    insert_voters_data_to_db(mock_conn, mock_cursor)
    mock_cursor.execute("SELECT * FROM voters")
    count = len(list(mock_cursor.fetchall()))

    #then

    assert count > 100
    assert mock_generate_voter_data.call_count == 2
    print(str(voter_id_2))
    delete_row_after_insert(mock_cursor, str(voter_id_2), str(voter_id_1))


'''


def test_create_tables_with_correct_properties():
    # given
    mock_conn = MagicMock()
    mock_cur = MagicMock()

    # when
    create_table_candidates(mock_conn, mock_cur)
    try:
        # then
        mock_cur.execute.assert_called_once_with(
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
        mock_conn.commit.assert_called_once()
    except Exception as e:
        pass


# configuration for db_test
DB_CONFIG = {
    "dbname": "my-db",
    "user": "kenne",
    "password": "kenne",
    "host": "192.168.178.194",
    "port": "5432"
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


def delete_row_after_insert(cur, id1, id2):
    try:
        cur.execute("DELETE FROM voters WHERE voter_id IN (%s, %s)", (id1, id2))
        cur.connection.commit()
        print("All records have been deleted from the votes table.")
    except Exception as e:
        cur.connection.rollback()
        print(f"An error occurred: {e}")
