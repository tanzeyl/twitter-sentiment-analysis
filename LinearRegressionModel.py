import tweepy
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt


def get_twitter_api():
    ACCESS_TOKEN = "1430185691506487311-T4ppr9guz9BtBsPMf4II8zRzVZAGDS"
    ACCESS_TOKEN_SECRET = "TzbCSch4nktm16yu6Wf7z5AiVwYOC5WWUiBRTg7ERyUiF"
    API_KEY = "VEDzqDFM9kdNTjTfnoncOlYOx"
    API_SECRET_KEY = "kSGCugLi1MnF4y5nVBYfRDWEI0Gzn61czlXlNlZ26ypuJ0JrGq"
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def collect_twitter_data(api, twitter_user):
    favorite_data = []
    retweet_data = []
    for tweets in tweepy.Cursor(api.user_timeline, id=twitter_user).items(100):
        favorite_data.append(tweets.favorite_count)
        retweet_data.append(tweets.retweet_count)
    return favorite_data, retweet_data


def main():
    api = get_twitter_api()
    favorite_data, retweet_data = collect_twitter_data(api, "@cnnbrk")
    print(favorite_data)
    print(retweet_data)
    retweet_data_col = np.array(retweet_data).reshape((-1, 1))
    print(retweet_data_col)
    lreg = linear_model.LinearRegression()
    lreg.fit(retweet_data_col, favorite_data)
    print("Coefficient: ", lreg.coef_)
    print("Intercepts: ", lreg.intercept_)

    x = np.array(range(0, max(retweet_data)))
    y = eval("lreg.coef_*x + lreg.intercept_")
    plt.plot(x, y)
    plt.scatter(retweet_data, favorite_data, color="red")
    plt.xlabel("Retweets")
    plt.ylabel("Favorites")
    plt.show()


if __name__ == "__main__":
    main()
