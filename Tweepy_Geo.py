import tweepy
import csv
import os

# These are the keys from the "Consumer Keys" section from your Twitter Devloper Portal
# Keep the "" when you paste in your keys

auth = tweepy.AppAuthHandler('consumer_key', 'consumer_secret')
api = tweepy.API(auth)

# Date should be formatted as YYYY-MM-DD
since_date = '2021-11-08'
until_date = '2021-11-11'

# Maximum number of results
max_tweets = 25

# Geocode of Lebanon, kansas plus a 1700 mile radius which would roughly be coast to coast
location = '39.8097,-98.5556,1700mi'

# Open/create a file to append data to
csvFile = open('result.csv', 'a')

# Writting Results to a csv
csvWriter = csv.writer(csvFile)

tweets = tweepy.Cursor(api.search_tweets,q='Dune', since=since_date, until=until_date).items(max_tweets)
for tweet in tweets:
    # Write a row to the CSV file
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    print(tweet.text, '\n')

csvFile.close()