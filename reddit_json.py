import praw
from praw.models import MoreComments
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

        ######################################################### Release date of movie ##################################################################
        date_entry = '2021-10-22'

        input_year, input_month, input_day = map(int, date_entry.split('-'))
        release_date = datetime(input_year, input_month, input_day)
        return release_date

def sentiment_check(sentence):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sentence)
    if float(ss['pos']) > float([ss['neg']]):
        return 'positive'
    else:
        return 'negative'

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

def write_to_json(stats_dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as input_dict:
        json.dump(stats_dictionary, input_dict, ensure_ascii=False, indent=4)

def append_to_dict(dictionary, submission, comments):
    dictionary['upvote_ratio'].append(submission.upvote_ratio)
    dictionary['score'].append(submission.score)
    dictionary['num_of_comments'].append(submission.num_comments)
    dictionary['titles'].append(submission.title)
    dictionary['comments'].append(comments)
    return dictionary

def total_sentiment_counts(dictionary):
    total_pos = 0
    total_neg = 0

    for count, title in enumerate(dictionary['titles']):
        if len(dictionary['comments'][count]) > 0:
            avg_comment_sentiment = get_sentiment_averages(dictionary['comments'][count])

            if float(avg_comment_sentiment['positive']) > float(avg_comment_sentiment['negative']):
                overall_comment_sentiment = 'positive'
            else:
                overall_comment_sentiment = 'negative'

            if title == 'positive' and overall_comment_sentiment == 'positive':
                total_pos += 1
            elif title == 'positive' and overall_comment_sentiment == 'negative':
                total_neg += 1
            elif title == 'negative' and overall_comment_sentiment == 'negative':
                total_pos += 1
            else:
                total_neg += 1

    pos_and_neg = {
        'pos' : total_pos,
        'neg' : total_neg
    }
    return pos_and_neg

if __name__ == "__main__":
    movie_name = ''

    # Login credentials for Reddit API
    reddit = praw.Reddit(
        client_id="Y9iVswQtUMulrMTo2SaBaA",
        client_secret="jSh1HQU6MklLa1N10gkUw4da9QB2Zw",
        user_agent="pc:movie_genie:v1.0 (by u/movie_genie)",
        )

    ######################################### Name of movie ##################################################################
    movie_name = 'Dune'
    
    release_date = get_movie_date(movie_name)

    before_dict = {
        'upvote_ratio' : [],
        'score' : [],
        'num_of_comments' : [],
        'titles' : [],
        'comments' : []
    }

    after_dict = {
        'upvote_ratio' : [],
        'score' : [],
        'num_of_comments' : [],
        'titles' : [],
        'comments' : []
    }

    completed_posts = 0

    # Loop through r/movies submissions searching by movie name - Adjust limit for number of results #########################
    for submission in reddit.subreddit('movies').search(query=movie_name, limit=10):

        completed_posts += 1
        print(f'Posts completed: {completed_posts} / 100')

        created_utc = (submission.created_utc)
        created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d')

        # Loop through top level num_of_comments in submission (post)
        comments = []

        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            comments.append(top_level_comment.body)
        if str(created_date) < str(release_date):
            before_dict = append_to_dict(before_dict, submission, comments)
        else:
            after_dict = append_to_dict(after_dict, submission, comments)

    print('Printing data to json files...')

    # Before release date (averages)
    before_ratio_total = round((sum(before_dict['upvote_ratio']) / len(before_dict['upvote_ratio']) * 100), 2)
    before_score_total = round(sum(before_dict['score']) / len(before_dict['score']), 2)
    before_comments_total = round(sum(before_dict['num_of_comments']) / len(before_dict['num_of_comments']), 2)
    before_sentiment = get_sentiment_averages(before_dict['titles'])
    before_sentiment_totals = total_sentiment_counts(before_dict)

    final_stats_before = {
        'Upvote Ratio' : before_ratio_total,
        'Posts' : before_score_total,
        'Comments' : before_comments_total,
        'Sentiment' : before_sentiment,
        'Positive Posts' : before_sentiment_totals['pos'],
        'Negative Posts' : before_sentiment_totals['neg']
    }

    write_to_json(final_stats_before, 'before_stats.json')

    # After release date (averages)
    after_ratio_total = round((sum(after_dict['upvote_ratio']) / len(after_dict['upvote_ratio']) * 100))
    after_score_total = round(sum(after_dict['score']) / len(after_dict['score']), 2)
    after_comments_total = round(sum(after_dict['num_of_comments']) / len(after_dict['num_of_comments']), 2)
    after_sentiment = get_sentiment_averages(after_dict['titles'])
    after_sentiment_totals = total_sentiment_counts(after_dict)

    final_stats_after = {
        'Upvote Ratio' : after_ratio_total,
        'Posts' : after_score_total,
        'Comments' : after_comments_total,
        'Sentiment' : after_sentiment,
        'Positive Posts' : after_sentiment_totals['pos'],
        'Negative Posts' : after_sentiment_totals['neg']
    }

    write_to_json(final_stats_after, 'after_stats.json')

    print('Done!')
