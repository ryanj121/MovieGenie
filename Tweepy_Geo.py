import tweepy
import csv

# These are the keys from the "Consumer Keys" section from your Twitter Devloper Portal
# Keep the "" when you paste in your keys

# !!!!! Test this out locally for now, do not upload any of your actual keys to github !!!!!
# https://developer.twitter.com/en/docs/authentication/guides/authentication-best-practices

auth = tweepy.OAuthHandler("key", "secret")

api = tweepy.API(auth)

# Geocode of Lebanon, kansas plus a 1700 mile radius which would roughly be coast to coast
search = api.search_tweets(q='Dune', count= 15, lang='en', geocode= '39.8097,-98.5556,1700mi')
for tweet in search:
    
    print(tweet.text, '\n')

# Date should be formatted as YYYY-MM-DD
# Search tweets by date
since_date = '2021-11-08'
until_date = '2021-11-11'
max_tweets = 150

tweets = tweepy.Cursor(api.search_tweets,q='Dune', since=since_date, until=until_date).items(max_tweets)

# Open/create a file to append data to
csvFile = open('result.csv', 'a')

# Writting Results to a csv
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search_tweets, q = "Dune", since = "2014-02-14", until = "2014-02-15",lang = "en").items(max_tweets):

    # Write a row to the CSV file
    csvWriter.writerow([tweet])
csvFile.close()