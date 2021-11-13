import tweepy

# These are the keys from the "Consumer Keys" section from your Twitter Devloper Portal
# Keep the "" when you paste in your keys

# !!!!! Test this out locally for now, do not upload any of your actual keys to github !!!!!
# https://developer.twitter.com/en/docs/authentication/guides/authentication-best-practices

auth = tweepy.AppAuthHandler("consumer key", "consumer key secret")

# Do not use "api.search_tweets" like in Tweepy's own example. Doesn't work for some reason

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q='movies').items(10):
    print(tweet.text)

searched_tweets = []
last_id = -1

query = 'python'
max_tweets = 100
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        break