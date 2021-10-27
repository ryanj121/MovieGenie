import tweepy

# These are the keys from the "Consumer Keys" section from your Twitter Devloper Portal
# Keep the "" when you paste in your keys

# !!!!! Test this out locally for now, do not upload any of your actual keys to github !!!!!
# https://developer.twitter.com/en/docs/authentication/guides/authentication-best-practices

auth = tweepy.AppAuthHandler("consumer key", "consumer key secret")

# Do not use "api.search_tweets" like in Tweepy's own example. Doesn't work for some reason

api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search, q='Enter Search Text Here').items(10):
    print(tweet.text)