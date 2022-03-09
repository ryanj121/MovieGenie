import csv
from imdb import IMDb


#creates an instance of the IMDB api to be used by methods
ia = IMDb()

# gets the worldwide gross of a movie
def movieGross():
    
    # Search movie by title from user input
    filmName = input("Enter name of movie: ")
    movie = ia.search_movie(filmName)
    gross_list = []
    # Take first result of serach
    id = movie[0].movieID  
    # Get Worldwide gross
    movie = ia.get_movie(id)
    gross = (movie['box office']['Cumulative Worldwide Gross'])
    # Remove "$" from result
    gross_num = gross[1:].split(", ")
    gross_number = gross_num[0]    
    return f'Worldwide Gross of {movie} is: ' + gross_number


# gets a persons ID to use in other IMDB api methods
def personID(name):
       
    person = ia.search_person(name)
    person_id = person[0].personID
    return person_id


# creates a list of all movies a certain actor is in
def get_actor_movies(personID):
    
    word2= 'id:'
    actor_name = ia.get_person(personID)
    x = str(actor_name['actor'])
    new_list=[]           
    for word in x.split():        
        if word2 in word:
            movie_ID = word[3:11].strip('[')
            movie_title = str(ia.get_movie(movie_ID))           
            new_list.append(movie_title)            
    return new_list


# uses the list created by get_actor_movie method to get the gross for all actors movies
def actor_movie_gross(movie_list):
    gross_actor = []    
    for movie in movie_list:
        try:
            x = movieGross(movie)
            gross_actor.append(x)
        except:
            pass    
    return gross_actor


# gets actors top 5 movies and averages them together
def gross_actor_average():
    actor_movie_gross.sort()
    return actor_movie_gross[-5:]

# gets date and formats it into a readable format for reddit
def get_date(filmName):
    list_of_months = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July':'07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December':'12'
    }
    movie = ia.search_movie(filmName)
    # Take first result of serach
    id = movie[0].movieID
    movie1 = ia.get_movie(id)
    ia.update(movie1, 'release dates')    
    date = (movie1['release dates'])
    movie_date = date[0]

    # Loops through the release dates and finds USA release, otherwise keeps first date
    for count, i in enumerate(date):
        temp_date1 = i.split()
        temp_date2 = temp_date1[0]
        country = temp_date2.split('::')[0]
        if country == 'USA':
            movie_date = date[count]
            break

    date2 = movie_date.split()
    day = date2[0]
    reddit_day = day.split('::')[1]
    reddit_month = date2[1]
    reddit_year = date2[2]
    for month in list_of_months:        
        if month == reddit_month:
            reddit_month = list_of_months[month]
    # date format YYYY-MM-DD
    return reddit_year + '-' + reddit_month + '-' + reddit_day


# tier list based on how many movies an actor has in the top 250 ranked movies in IMDB
def actor_tier(count):    
    if count>= 4:
        return 'A'    
    if count < 4 and count >= 3:
        return 'B'    
    if count< 3 and count >= 2:
        return 'C'    
    if count < 2:
        return 'D'

#gets the top 250 ranked movies from IMDB
def get_top_movies():
    title_list = []
    search = ia.get_top250_movies()
    for i in range(250):
        x = search[i]['title']
        title_list.append(x)
    return title_list
    

#gets the top 8 actors listed for each movie in the top 250
def get_top_movie_cast(title_list):
    actor_movie_str = []
    test_list = []    
    for i in title_list:
        movie1 = ia.search_movie(i)
        id = movie1[0].movieID    
        movie = ia.get_movie(id)
        test_list.append(movie1[0]['title'])        
        if movie:
            cast = movie.get('cast')
            topActors = 8
            for actor in cast[:topActors]:
                test_list.append(actor['name'])        
    for i in test_list:
        lower1 = str(i).lower()
        actor_movie_str.append(lower1)         
    return actor_movie_str


# wrties the list of actors for the top 250 movies into a csv file for easy and efficient access
def write_list_file(list):
    start = 0
    finish = 9
    with open('top_250.csv', 'w', ) as file1:
        writer = csv.writer(file1)
        for i in list:
            list1 = list[start:finish]
            writer.writerow(list1)
            start += 9
            finish += 9
        file1.close() 


# this counts the times an actor appears in the list of 250 movies
def search_list_actor():
    actor = input('Enter Actor: ').lower()
    count = 0
    with open('top_250.csv') as file2:
        csvreader = csv.reader(file2, delimiter=',')
        for row in csvreader:
            #actor.lower
            if actor in row:
                count+=1
    return count

def lower_data():
    with open('d3.tsv', encoding="utf-8") as file2:
        csvreader = csv.reader(file2, delimiter='\t')
        with open('data_lower.csv', 'w', newline='', encoding="utf-8") as file3:
            csvwriter = csv.writer(file3, delimiter='\t')
            for row in csvreader:
                actor_row = row[1].lower()
                actor_movie_row = row[5]
                csvwriter.writerow([actor_row, actor_movie_row])
              
def actor_known_titles():
        with open('actor_known_titles.csv',encoding="utf-8") as file3:
            csvreader = csv.reader(file3, delimiter='\t')
            for row in csvreader:
                list = row[1].split(',')
                

            

# need to search for actor name, grab 6th column in csv
# convert it to names instead of ID
def actor_top_movies():
    actor = input('Enter Actor: ')
    with open('data_lower.csv', encoding="utf-8") as file2:
        csvreader = csv.reader(file2, delimiter='\t')
        for row in csvreader:
            if actor in row:
                movie_ids = row[1].split(',')
                for i in movie_ids:
                    id = i.strip('tt')
                    top_movie = ia.get_movie(id)
                    print(top_movie)

#print(search_list_actor())
#print(movieGross())
# needs to lowercase so it will find actor in csv file
#movie = input('Enter Movie: ')
#actor = input('Enter Actor: ').lower()

#print(get_date(movie))

#print(f'{actor} was in',search_list_actor(actor), 'top 250 movies')
#print(f'Based on our ranking system {actor} is a ' + actor_tier(search_list_actor(actor)) + ' tier actor')
#list1 = get_top_movie_cast(get_top_movies())
#write_list_file(list1)
#print(get_top_movie_cast(get_top_movies()))
#print(type(list(get_top_movie_cast(get_top_movies()))))
#x = personID(input_name)
#var2 = get_actor_movies(x)
#var3 = actor_movie_gross(var2)
# var3.sort()
# sum_of_gross = sum(var3[-5:])
# average_gross = sum_of_gross/10
# print(average_gross)
# print(actor_tier(average_gross))

