from imdb import IMDb

# Create an instance of the IMDb class

ia = IMDb()

# Search movie by title
input_name = input("Enter name of movie: ")
search = ia.search_movie(input_name)

# Enter in desired year of release
input_year = input("Enter year of release: ")

# Loop through list of search results

for i in range(len(search)):
    id = search[i].movieID
    year = search[i]['year']

    # Prints a result only if the names match exactly and the year matches

    if (input_year == str(year)) and (input_name == str(search[i]['title'])):
        print(search[i]['title'] + " : " + id + " Year: " + str(year))