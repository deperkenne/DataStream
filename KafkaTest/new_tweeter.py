import tweepy #pip3 install tweepy
# Create twitter account, if you don't have one
# Generate API & Access tokens from the link below
# https://developer.twitter.com/, Navigate to Apps and app name to generate all keys & secrets
API_KEY = "392RBSZhdobmfdLll61yZc3fj"
API_SECRET = "ihYKhMIEdi2TGVSCMY76s6mJtuMex24K1bHMy4uUc9dvX0dcSu"
ACCESS_TOKEN = "1873676695342837760-3relr3veljcDIGv17aX2pl2B6L9APR"
ACCESS_TOKEN_SECRET = "tdWlUA9uvYyUDNorQFgetQXeBdzQnH7GotGeqdxtnPFnu"
# Authenticate and make sure your keys work
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)
# api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")



# Check for latest 100 tweets with hashtag python or orskl
tweets = api.search(q="Python", lang="en", rpp=100)
for tweet in tweets:
    USER = tweet.user.name
    RETWEETS = tweet.retweet_count
    CREATED = tweet.created_at
    TEXT = tweet.text
    SOURCE = tweet.source
    print(USER + " | " + TEXT + " | " + str(CREATED) + " | " + str(RETWEETS) + " | " + SOURCE)


# Create a class that listens streaming tweets with hashtag python or orskl
# Refer to https://docs.python.org/3/tutorial/classes.html for details on Python classes

class OrSklStream(tweepy.StreamListener):
    # Class inheritance as we discussed in Track 1 Intro session
    # Inherting tweepy.StreamListener class in to OrSklStream class
    # More info on inheritances - https://docs.python.org/3/tutorial/classes.html#inheritance

    def __init__(self, passed_api):
        self.api = passed_api
        self.me = api.me()

    # Lets transform the data and store them in flat file
    def on_status(self, tweet):
        USER = tweet.user.name
        RETWEETS = tweet.retweet_count
        CREATED = tweet.created_at
        TEXT = tweet.text
        SOURCE = tweet.source
        print(USER + " | " + TEXT + " | " + str(CREATED) + " | " + str(RETWEETS) + " | " + SOURCE)
        file = open('./Track 5 | Python Data Engineering | Streaming data | Extract & Transform/tweets_extract.csv', "a")
        output = USER + " | " + TEXT + " | " + str(CREATED) + " | " + str(RETWEETS) + " | " + SOURCE + '\n'
        file.write(output)
        file.close()

# Let this run in PyCharm and test
tweets_listener = OrSklStream(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Orskl"], languages=["en"])

# Run the code in the background and verify data flowing in
