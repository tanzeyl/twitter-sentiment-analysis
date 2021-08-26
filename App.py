import numpy as np
import joblib
from flask import Flask, render_template, request
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        consumer_key = 'VEDzqDFM9kdNTjTfnoncOlYOx'
        consumer_secret = 'kSGCugLi1MnF4y5nVBYfRDWEI0Gzn61czlXlNlZ26ypuJ0JrGq'
        access_token = '1430185691506487311-T4ppr9guz9BtBsPMf4II8zRzVZAGDS'
        access_token_secret = 'TzbCSch4nktm16yu6Wf7z5AiVwYOC5WWUiBRTg7ERyUiF'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=25):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

# api = TwitterClient()
# tweets = api.get_tweets(query='Donald Trump', count=200)
# ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
# ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# all_tweets = [ptweets, ntweets]
# return all_tweets


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/search", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        api = TwitterClient()
        query = str(request.form.get("query"))
        tweets = api.get_tweets(query = query, count = 25)
        for tweet in tweets:
            if "retweeted_status" in tweet:
                tweet = tweet["retweeted_status"]
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        all_tweets = [ptweets, ntweets]
        return render_template('index.html', your_list = all_tweets)


if __name__ == "__main__":
    app.run(debug=True)
