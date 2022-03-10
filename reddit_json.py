from webbrowser import get
import praw
from praw.models import MoreComments
from datetime import datetime
# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import subjectivity
# from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk import tokenize
import json
from movie_code import get_date

# Returns movie release date
# def get_movie_date():
        #date_entry = '2021-10-22'
        #input_year, input_month, input_day = map(int, date_entry.split('-'))
        #release_date = datetime(input_year, input_month, input_day)
        #return release_date

# Returns movie name
# def get_movie_name(movie_name):
#    movie_name = 'Dune'
#    return movie_name

# Uses nltk to measure sentiment of each total pos/neg socres for each thread, returns an overall pos/neg
def sentiment_check(sentence):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sentence)
    if float(ss['pos']) > float([ss['neg']]):
        return 'positive'
    else:
        return 'negative'

# Uses nltk to analyse the sentiment of individual comments
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

    if len(sentences) > 0:
        negative_average = negative_total / len(sentences)
        neutral_average = neutral_total / len(sentences)
        positive_average = positive_total / len(sentences)

        averages_dict = {
            'negative': negative_average,
            'neutral' : neutral_average,
            'positive' : positive_average
        }
    else:
        averages_dict = {}
    return averages_dict

# Writes a dictionary to a json file
def write_to_json(stats_dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as input_dict:
        json.dump(stats_dictionary, input_dict, ensure_ascii=False, indent=4)

# Inserts reddit search results into initial dictionaries
def append_to_dict(dictionary, submission, comments):
    dictionary['upvote_ratio'].append(submission.upvote_ratio)
    dictionary['score'].append(submission.score)
    dictionary['num_of_comments'].append(submission.num_comments)
    dictionary['titles'].append(submission.title)
    dictionary['comments'].append(comments)
    return dictionary

# Returns the total number of pos/neg comments in a thread
def total_sentiment_counts(dictionary):

    pos_and_neg = {}
    total_pos = 0
    total_neg = 0
    weighted_pos = 0
    weighted_neg = 0

    for count, title in enumerate(dictionary['titles']):
        if len(dictionary['comments'][count]) > 0:
            avg_comment_sentiment = get_sentiment_averages(dictionary['comments'][count])

            if float(avg_comment_sentiment['positive']) > float(avg_comment_sentiment['negative']):
                total_pos += 1
                weighted_pos += len(dictionary['comments'][count])
            else:
                total_neg += 1
                weighted_neg += len(dictionary['comments'][count])

    pos_and_neg = {
        'pos' : total_pos,
        'neg' : total_neg,
        'pos_score' : weighted_pos,
        'neg_score' : weighted_neg
    }
    return pos_and_neg

# Setup dictionaries for initial returns from reddit
def init_dict(dict):
    dict = {
        'upvote_ratio' : [],
        'score' : [],
        'num_of_comments' : [],
        'titles' : [],
        'comments' : []
    }
    return dict

# Setup dictionaries for the final stats including sentiment scores
def init_final_dict(input_dict):
    if len(input_dict['upvote_ratio']) > 0:
        ratio_total = round((sum(input_dict['upvote_ratio']) / len(input_dict['upvote_ratio']) * 100), 2)
    else:
        ratio_total = 0

    if len(input_dict['score']) > 0:
        score_total = round(sum(input_dict['score']) / len(input_dict['score']), 2)
    else:
        score_total = 0

    if len(input_dict['num_of_comments']) > 0:
        comments_total = round(sum(input_dict['num_of_comments']) / len(input_dict['num_of_comments']), 2)
    else:
        comments_total = 0

    sentiment = get_sentiment_averages(input_dict['titles'])
    sentiment_totals = total_sentiment_counts(input_dict)

    if len(input_dict) > 0:
        final_stats_dict = {
            'Upvote Ratio' : ratio_total,
            'Posts' : score_total,
            'Comments' : comments_total,
            'Sentiment' : sentiment,
            'Positive Posts' : sentiment_totals['pos'],
            'Negative Posts' : sentiment_totals['neg'],
            'Weighted Positive' : sentiment_totals['pos_score'],
            'Weighted Negative Score' : sentiment_totals['neg_score']
        }
    else:
        final_stats_dict = {}

    return final_stats_dict


def get_movie_sentiment_scores(movie_name):
    # Login credentials for Reddit API
    reddit = praw.Reddit(
        client_id="Y9iVswQtUMulrMTo2SaBaA",
        client_secret="jSh1HQU6MklLa1N10gkUw4da9QB2Zw",
        user_agent="pc:movie_genie:v1.0 (by u/movie_genie)",
        )

    # Set a maximum number of results to protect against large values
    # if limit_results > 25:
    limit_results = 25

    release_date = get_date(str(movie_name))
    # print(release_date)

    before_dict = {}
    after_dict = {}

    before_dict = init_dict(before_dict)
    after_dict = init_dict(after_dict)

    completed_posts = 0

    # Loop through r/movies submissions searching by movie name - Adjust limit for number of results
    for submission in reddit.subreddit('movies').search(query=movie_name, limit=limit_results):

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

        completed_posts += 1
        # print(f'Posts completed: {completed_posts} / {limit_results}')

    if len(before_dict) > 0:
        final_stats_before = init_final_dict(before_dict)
    
    if len(after_dict) > 0:
        final_stats_after = init_final_dict(after_dict)

    write_to_json(final_stats_before, 'before_stats.json')
    write_to_json(final_stats_after, 'after_stats.json')
    
    #### Return a list of both dictionaries
    return [final_stats_before, final_stats_after]

# Start main program
# if __name__ == "__main__":
#    get_movie_sentiment_scores('Dune')