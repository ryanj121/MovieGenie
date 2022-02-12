import praw
import time
from datetime import datetime
import csv
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import json

def get_movie_date(movie_name):

        # Release date of movie ##################################################################
        date_entry = '2021-10-22'

        input_year, input_month, input_day = map(int, date_entry.split('-'))
        release_date = datetime(input_year, input_month, input_day)
        return release_date

def get_sentiment_averages(sentences):
    negative_total = 0
    neutral_total = 0
    positive_total = 0

    for sentence in sentences:
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence)
        negative_total += ss['neg']
        neutral_total += ss['neu']
        positive_total += ss['pos']

    negative_average = negative_total / len(sentences)
    neutral_average = neutral_total / len(sentences)
    positive_average = positive_total / len(sentences)

    averages_dict = {
        'negative': negative_average,
        'neutral' : neutral_average,
        'positive' : positive_average
    }
    return averages_dict

if __name__ == "__main__":
    movie_name = ''

    # Login credentials for Reddit API
    reddit = praw.Reddit(
        client_id="Y9iVswQtUMulrMTo2SaBaA",
        client_secret="jSh1HQU6MklLa1N10gkUw4da9QB2Zw",
        user_agent="pc:movie_genie:v1.0 (by u/movie_genie)",
        )

    # Name of movie ##################################################################
    movie_name = 'Dune'
    
    release_date = get_movie_date(movie_name)
    before_upvotes = []
    before_score = []
    before_comments = []
    before_titles = []

    after_upvotes = []
    after_score = []
    after_comments = []
    after_titles = []


    for submission in reddit.subreddit('movies').search(query=movie_name):

        created_utc = (submission.created_utc)
        created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d')

        if str(created_date) < str(release_date):
            before_upvotes.append(submission.upvote_ratio)
            before_score.append(submission.score)
            before_comments.append(submission.num_comments)
            before_titles.append(submission.title)

        else:
            after_upvotes.append(submission.upvote_ratio)
            after_score.append(submission.score)
            after_comments.append(submission.num_comments)
            after_titles.append(submission.title)

    # Before release date (averages)
    before_ratio_total = round((sum(before_upvotes) / len(before_upvotes) * 100), 2)
    before_score_total = round(sum(before_score) / len(before_score), 2)
    before_comments_total = round(sum(before_comments) / len(before_comments), 2)
    before_sentiment = get_sentiment_averages(before_titles)

    final_stats_before = {
        'Ratio' : before_ratio_total,
        'Posts' : before_score_total,
        'Comments' : before_comments_total,
        'Sentiment' : before_sentiment
    }

    json_string = json.dumps(final_stats_before)
    with open('before_stats.json', 'w') as input_dict:
        json.dump(json_string, input_dict)

    # After release date (averages)
    after_ratio_total = round((sum(after_upvotes) / len(after_upvotes) * 100))
    after_score_total = round(sum(after_score) / len(after_score), 2)
    after_comments_total = round(sum(after_comments) / len(after_comments), 2)
    after_sentiment = get_sentiment_averages(after_titles)

    final_stats_after = {
        'Ratio' : after_ratio_total,
        'Posts' : after_score_total,
        'Comments' : after_comments_total,
        'Sentiment' : after_sentiment
    }

    json_string = json.dumps(final_stats_after)
    with open('after_stats.json', 'w') as input_dict:
        json.dump(json_string, input_dict)
