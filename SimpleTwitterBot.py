import tweepy

ACCESS_TOKEN = "1430185691506487311-T4ppr9guz9BtBsPMf4II8zRzVZAGDS"
ACCESS_TOKEN_SECRET = "TzbCSch4nktm16yu6Wf7z5AiVwYOC5WWUiBRTg7ERyUiF"
API_KEY = "VEDzqDFM9kdNTjTfnoncOlYOx"
API_SECRET_KEY = "kSGCugLi1MnF4y5nVBYfRDWEI0Gzn61czlXlNlZ26ypuJ0JrGq"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
api.update_status(status = "Hello World")