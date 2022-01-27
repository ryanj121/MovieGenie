import praw
import time
from datetime import datetime
import csv

def get_movie_date(movie_name):

        # Input release date
        date_entry = input('Release date in YYYY-MM-DD format: ')
        input_year, input_month, input_day = map(int, date_entry.split('-'))
        release_date = datetime(input_year, input_month, input_day)
        return release_date

def write_to_files():

    # Name headers of csv files
    csvFile = open('reddit_before.csv', 'a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['title', 'upvotes', 'upvote ratio', 'comments', 'created date'])

    csvFile = open('reddit_after.csv', 'a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['title', 'upvotes', 'upvote ratio', 'comments', 'created date'])

    # Subbmissions before release date
    for submission in reddit.subreddit('movies').search(query=movie_name):
        
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

if __name__ == "__main__":
    movie_name = ''
    movie_menu = ''

    # Login credentials for Reddit API
    reddit = praw.Reddit(
        client_id="Y9iVswQtUMulrMTo2SaBaA",
        client_secret="jSh1HQU6MklLa1N10gkUw4da9QB2Zw",
        user_agent="pc:movie_genie:v1.0 (by u/movie_genie)",
        )

    while movie_name.lower() != 'quit':

        # Input name of movie
        print('\nType "quit" to quit')
        movie_name = input('Enter name of movie: ')

        if movie_name.lower() == 'quit':
            break

        release_date = get_movie_date(movie_name)

        while movie_menu.lower() != 'back':
            print('\nType "back" to return to main menu')
            print('Options:')
            print('1. Write before/after posts to file')
            print('2. Display before/after metrics')
            movie_menu = input()

            if movie_menu.lower() == 'back':
                break

            if movie_menu == '1':
                write_to_files(movie_name)

            elif movie_menu == '2':
                before_upvotes = []
                before_score = []
                before_comments = []

                after_upvotes = []
                after_score = []
                after_comments = []


                for submission in reddit.subreddit('movies').search(query=movie_name):
        
                    created_utc = (submission.created_utc)
                    created_date = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d')

                    if str(created_date) < str(release_date):
                        before_upvotes.append(submission.upvote_ratio)
                        before_score.append(submission.score)
                        before_comments.append(submission.num_comments)
                    else:
                        after_upvotes.append(submission.upvote_ratio)
                        after_score.append(submission.score)
                        after_comments.append(submission.num_comments)

                print('\n*** Before release date (averages) ***')
                print(f'Upvote Ratio: {round((sum(before_upvotes) / len(before_upvotes) * 100), 2)} %')
                print(f'Total Votes: {round(sum(before_score) / len(before_score), 2)}')
                print(f'Comments: {round(sum(before_comments) / len(before_comments), 2)}')

                print('\n*** After release date (averages) ***')
                print(f'Upvote Ratio: {round((sum(after_upvotes) / len(after_upvotes) * 100), 2)} %')
                print(f'Total Votes: {round(sum(after_score) / len(after_score), 2)}')
                print(f'Comments: {round(sum(after_comments) / len(after_comments), 2)}')
