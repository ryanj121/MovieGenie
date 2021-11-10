from imdb import IMDb

# Create an instance of the IMDb class

ia = IMDb()

# Get Worldwide gross for movie by IMDb ID number

movie = ia.get_movie(4154796)
print(movie['box office']['Cumulative Worldwide Gross'])

# Searches for a movie by name and creates a list named 'search' with all IMDb entries with that name

name = 'Avengers: End Game'
search = ia.search_movie(name)

# Loops through the 'search' list and prints 'Movie Name : IMDb ID number'

for i in range(len(search)):
    id = search[i].movieID
    print(search[i]['title'] + " : " + id)

# Test Comment for GitHub source control changes