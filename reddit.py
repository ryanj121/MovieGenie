import praw
import time
from datetime import datetime
import csv

# Login credentials for Reddit API
reddit = praw.Reddit(
    client_id="Y9iVswQtUMulrMTo2SaBaA",
    client_secret="jSh1HQU6MklLa1N10gkUw4da9QB2Zw",
    user_agent="pc:movie_genie:v1.0 (by u/movie_genie)",
)

# Input name of movie
input_movie = input('\nEnter name of movie: ')

# Input release date
date_entry = input('Release date in YYYY-MM-DD format: ')
input_year, input_month, input_day = map(int, date_entry.split('-'))
release_date = datetime(input_year,input_month, input_day)

# Name headers of csv files
csvFile = open('reddit_before.csv', 'a')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['title', 'upvotes', 'upvote ratio', 'comments', 'created date'])

csvFile = open('reddit_after.csv', 'a')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['title', 'upvotes', 'upvote ratio', 'comments', 'created date'])

# Subbmissions before release date
for submission in reddit.subreddit('movies').search(query=input_movie):
    
    created_utc = (submission.created_utc)
    created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d')

    if str(created_date) < str(release_date):
        csvFile = open('reddit_before.csv', 'a')
    else:
        csvFile = open('reddit_after.csv', 'a')

    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([submission.title, 
        submission.score, 
        submission.upvote_ratio, 
        submission.num_comments, 
        created_date])
