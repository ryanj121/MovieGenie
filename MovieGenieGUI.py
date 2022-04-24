from msilib.schema import ComboBox
from tkinter import *
from imdb import IMDb
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from redditCode import *
import json


# Create an instance of the IMDb class
ia = IMDb()
#The xaxis will serve as the list of movies input by the user
xaxis=[]
#The yaxis will contain the corresponding list of revenues for the user input movies
yaxis=[]

# function to run menu option
def menuopt(event):
  selection = choice.get()
  if (selection == "revenue"):
    movieGross()
  elif (selection == "reddit"):
    reddit()
  elif (selection == "filmography"):
    filmography()
  return None

#Audience centiment function using reddit
# gets date and formats it into a readable format for reddit
def reddit():
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
    filmName = search.get()
    movie = ia.search_movie(filmName)
    filmName = (movie[0]['title'])
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
    redDate = reddit_year + '-' + reddit_month + '-' + reddit_day
    before, after = get_movie_sentiment_scores(filmName, redDate)
    before = str(before)
    after = str(after)
    before = before.replace(',', '\n')
    after = after.replace(',', '\n')
    text.insert(1.0, before)
    text.insert(1.0, "\n" + "\n")
    text.insert(1.0, after)
    
#The movieGross method finds the gross revenue of the input movie and adds the movie and its 
#revenue to the appropriate lists
def movieGross(): 
    title = search.get()
    movie = ia.search_movie(title)
    title=(movie[0]['title'])
        
    # Take result of search and find gross revenue
    id = movie[0].movieID
    # Get Worldwide gross
    movie = ia.get_movie(id)
    gross = (movie['box office']['Cumulative Worldwide Gross'])

    # format result
    global gross_num
    gross_num = (gross[1:])
    gross_num=gross_num.partition(" ")
    gross_num=gross_num[0]
    gross_num=gross_num[:-1] if gross_num[-1]==',' else gross_num
    text.insert(1.0, "Worldwide gross of " + title + ":  $" + gross_num + "\n")
    gross_num=int(gross_num.replace(',', ''))
    global xaxis
    global yaxis
    xaxis.append(title)
    yaxis.append(gross_num)
    return None

def personID(name):
    ia = IMDb()
    name = ia.search_person(name)
    person_id = name[0].personID
    return person_id

#filmography method will find the list of movies an actor was in
def filmography():
  actor=search.get()
  actorID=personID(actor)
  ia = IMDb()
  word2= 'id:'
  actor_name = ia.get_person(actorID)
  x = str(actor_name['actor'])
  new_list2=[]         
  for word in x.split():        
      if word2 in word:
          movie_ID = word[3:11].strip('[')
          movie_title = str(ia.get_movie(movie_ID))
          new_list2.append(movie_title)
          for item in new_list2:
            text.insert(1.0, item + "\n")
  return None

#The movieChart method will create a bar chart from the created list of movies and revenue   
def movieChart():
  plt.figure(figsize=(10, 6))
  plt.title("Gross Box Office Revenue")
  plt.ylim(min(yaxis)-100000, max(yaxis)+300000000)
  plt.bar(xaxis, yaxis)
  plt.yticks(np.arange(min(yaxis)-min(yaxis)%100000000, max(yaxis)-max(yaxis)%100000000+100000000, 100000000))
  current_values=plt.gca().get_yticks()
  plt.gca().set_yticklabels(['${:,.0f}'.format(x) for x in current_values])
  plt.grid(which='major', axis='y')
  plt.grid(which='minor', axis='y')
  plt.show()

  #gets the top 250 ranked movies from IMDB
def get_top_movies():
    title_list = []
    search = ia.get_top250_movies()
    for i in range(250):
        x = search[i]['title']
        title_list.append(x)
    for j in title_list:
      text.insert(1.0, j + "\n")
    return None
  


#clearbox method clears the search box when the search box is clicked on.
def clearbox(event):
    search.delete(0,"end")
    return None

#clrLists method clears the stored lists of movies and revenue
def clrLists():
  xaxis.clear()
  yaxis.clear()
  text.delete(1.0, "end")

#Configure Main Window
mainWindow=Tk()
mainWindow.configure(bg="magenta")
mainWindow.geometry("800x650")

#Place MovieGenie Logo
logo=Image.open('LogoMG.png')
logo=logo.resize((200, 200))
logo=ImageTk.PhotoImage(logo)
chart=Image.open('chartButton.png')
chart=chart.resize((50, 50))
chart=ImageTk.PhotoImage(chart)
boxReset=Image.open('resetButton.png')
boxReset=boxReset.resize((50, 50))
boxReset=ImageTk.PhotoImage(boxReset)


#display Heading
heading=Label(mainWindow, text="MovieGenie", bg="magenta", font=("ALGERIAN", 60))
heading.place(x=100, y=25)

#variables to create dropdown menu
options=["revenue", "reddit", "filmography"]
choice=StringVar()
choice.set(options[0])

#Create entry box for movie title
search=Entry(mainWindow, width=55,)
search.place(x=150, y=150)
search.insert(0, "Enter Actor or Movie Title and Select Option")

#Create text box to return results
tframe=Frame(mainWindow)
tscroll=Scrollbar(tframe, orient=VERTICAL)
text=Text(tframe, width=60, height=20, yscrollcommand=tscroll.set)
tscroll.config(command=text.yview)
tscroll.pack(side=RIGHT, fill=Y)
tframe.place(x=150, y=220)
text.pack()

#Calling the clearbox method to clear the search box
search.bind("<Button-1>", clearbox)

usermenu=OptionMenu(mainWindow, choice, *options, command=menuopt)
usermenu.place(x=460, y=146)

#Button to clear text box and lists
button2=Button(mainWindow, image=boxReset, command=clrLists, borderwidth=0)
button2.place(x=70, y=230)
#Button to call movieChart function and create chart
button3=Button(mainWindow, image=chart, command=movieChart, borderwidth=0)
button3.place(x=71, y=310)

#Button to get top 250 movies
button6=Button(mainWindow, image=logo, command=get_top_movies, borderwidth=0)
button6.image=logo
button6.place(x=565, y=10)

mainWindow.mainloop()
