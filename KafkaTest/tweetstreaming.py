
from ntscraper import Nitter
from pprint import pprint
import random
import json


scraper = Nitter(log_level= 1,skip_instance_check=False)
tweets = scraper.get_tweets("python",mode="hashtag",number=10)
pprint(tweets)







