import pytest
from sqlalchemy.testing.plugin.plugin_base import assertions
from sparkstream.votingApp.insertdatatotables import *




def test_return_correctly_list_of_candidates():
    # given
    BASE_URL = 'https://randomuser.me/api/?nat=gb'
    list_gender_expected = setUpListCandidates()
    i = 0


    while i < 3:
        # when SUT
        list_candidate = get_data(BASE_URL)
        list_genders = list(map(lambda candidate: candidate["gender"],list_candidate))
        # then
        assert set(list_gender_expected) == set(list_genders),"error not same containt"
        i = i +1


def setUpListCandidates():
    return ["male","male","female"]








