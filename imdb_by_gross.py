from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Search movie by title from user input
input_name = input("Enter name of movie: ")
movie = ia.search_movie(input_name)

# Take first result of serach
id = movie[0].movieID
print(movie[0]['title'] + " : " + id)

# Get Worldwide gross
movie = ia.get_movie(id)
gross = (movie['box office']['Cumulative Worldwide Gross'])

# Remove "$" from result
gross_num = (gross[1:])
print("Worldwide gross of first result: " + gross_num)

input_name = input("Enter name of movie: ")
movie2 = ia.search_movie(input_name)

highest_gross = 0

# Loop through serch results to find movie with highest gross
for i in range(len(movie2)):
    id = movie2[i].movieID
    movie_id_num = ia.get_movie(id)

    print(movie2[i]['title'] + " : " + id)
    gross = (movie_id_num[i]['box office']['Cumulative Worldwide Gross'])
    gross_num = (gross[1:])

    # If current movie's gross is the highest, set to highest_gross
    if gross_num > highest_gross:
        highest_gross = gross_num
        highest_movie = id

print(id['box office']['Cumulative Worldwide Gross'])