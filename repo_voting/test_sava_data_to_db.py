import pytest

from .insertdatatotables import get_data



BASE_URL = 'https://randomuser.me/api/?nat=gb'


@pytest.mark.parametrize("url,expected_list", [
    (BASE_URL,["male","male","female"] ),
    (BASE_URL, ["male", "male", "female"] ),
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












