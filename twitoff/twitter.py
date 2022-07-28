'''
Handles connection to Tiwtter API using Tweepy
'''
from os import getenv
import tweepy
import spacy
from twitoff.models import DB, Tweet, User

# Get API Key from environment vars.
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load('my_model')


def add_or_update_user(username):
    '''Takes username and pulls user from Twitter API'''
    twitter_user = TWITTER.get_user(screen_name=username)
    # Is there a user in the database that already has this id?
    # If not, then create a User in the database with this id.
    db_user = (User.query.get(twitter_user.id))
    if db_user is None:
        db_user = User(id=twitter_user.id, username=username)
        # add the user to the dßatabase.
        DB.session.add(db_user)

    # Get user's tweets
    tweets = twitter_user.timeline(
        count=200,
        exclude_replies=True,
        include_rts=False,
        tweet_mode='extended'
    )

    # Add each tweet to the DB
    for tweet in tweets:
        db_tweet = Tweet(
            id=tweet.id, 
            text=tweet.full_text,
            vector=vectorize_tweets(tweet.full_text)
        )
        if Tweet.query.get(db_tweet.id) is None:
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    
    DB.session.commit()


def vectorize_tweets(tweet_text):
    '''Make a vector from text'''
    return nlp(tweet_text).vector


def update_all_users():
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)
    
    return usernames