def movieGross(filmName):
    from imdb import IMDb
    
    # Create an instance of the IMDb class
    ia = IMDb()

    # Search movie by title from user input
    #input_name = input("Enter name of movie: ")
    movie = ia.search_movie(filmName)

    # Take first result of serach
    id = movie[0].movieID
    print(movie[0]['title'] + " : " + id)
    # Get Worldwide gross
    movie = ia.get_movie(id)
    gross = (movie['box office']['Cumulative Worldwide Gross'])

    # Remove "$" from result
    gross_num = (gross[1:])
    result="Worldwide gross of " + filmName + ":   $" + gross_num
    return(result)
   