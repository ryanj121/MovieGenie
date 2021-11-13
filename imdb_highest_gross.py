from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Input name of movie
input_name = input("\nEnter name of movie: ")
search = ia.search_movie(input_name)

# Input year of movie
input_year = input("Enter year of release: ")

highest_gross = 0
gross_num = 0
results = 0

# Loop through search results to find movie with highest gross
for i in range(len(search)):

    try:
        # Only excecute if movie's year matches and the title is exactly the same
        # This eliminates different movies with the same words in the title being compared
        if (input_year == str(search[i]['year'])) and (input_name == str(search[i]['title'])):
            id = search[i].movieID
            movie = ia.get_movie(id)

            results += 1

            print('\n' + 'Result number ' + str(results))
            print(search[i]['title'] + " : " + id)

            # Not every movie has a dictionary entry for 'Cumulative Worldwide Gross'
            # This will keep the program running in this case
            try:
                print(movie['box office']['Cumulative Worldwide Gross'])
                gross = str((movie['box office']['Cumulative Worldwide Gross']))

                # Strips commas from gross
                gross = gross.replace(',', '')

                # Splits name from other data that is sometimes returned (date of release)
                gross = gross.split(' ')[0]
                print(gross)

                #Strips leading "$" that is returned
                gross_num = float(gross[1:])
            except KeyError:
                print('No box office information')
            # If current movie's gross is the highest, set to highest_gross
            if  gross_num > highest_gross:
                highest_gross = gross_num
                highestMovie = movie
    except KeyError:
        print("No year data")

# Results will remain at 0 if no movies matched input_name and input_year
if results > 0:
    # Print results of the movie's gross
    print('\nThe hightest grossing movie with the title of ' + input_name + ' from the year ' + input_year)
    print('Title: ' + highestMovie['title'])
    print('Worldwide box office: ' + highestMovie['box office']['Cumulative Worldwide Gross'])

    # Print 'Opening Weekend United States' if it exists in the movie's dictionary
    try:
        print('Opening US Weekend: ' + highestMovie['Opening Weekend United States'])
    except KeyError:
        print('Opening US Weekend: No data')
else:
    print('\nThere are no movies titled ' + input_name + ' from ' + input_year + '\n')