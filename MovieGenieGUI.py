from tkinter import *
from imdb import IMDb
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
# Create an instance of the IMDb class
ia = IMDb()
#The xaxis will serve as the list of movies input by the user
xaxis=[]
#The yaxis will contain the corresponding list of revenues for the user input movies
yaxis=[]

#The movieGross method finds the gross revenue of the input movie and adds the movie and its 
#revenue to the appropriate lists
def movieGross(): 
    # Search movie by title from user input
    #input_name = input("Enter name of movie: ")
    title=search.get()
    movie = ia.search_movie(title)
    title=(movie[0]['title'])
        
    # Take result of search and find gross revenue
    id = movie[0].movieID
    print(movie[0]['title'] + " : " + id)
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
    xaxis.append(title)
    yaxis.append(gross_num)
    return None

#filmography method will find a the list of movies an actor was in
#def filmography():
#  actor=actorName.get()
#  castMember=ia.search_person(actor)
#  actor=(castMember[0], ['name'])
#  id=castMember[0].personID
#  films=ia.get_person_filmography(id)
#  for job in castMember ['filmography'].keys():

#  movieList=(films['filmography'])
#  print(movieList)

#The movieChart method will create a bar chart from the created list of movies and revenue   
def movieChart():
  plt.figure(figsize=(10, 6))
  plt.title("Gross Box Office Revenue")
  plt.ylim(min(yaxis)-10000000, max(yaxis)+10000000)
  plt.bar(xaxis, yaxis)
  plt.yticks(np.arange(min(yaxis)-min(yaxis)%100000000, max(yaxis)-max(yaxis)%100000000+100000000, 100000000))
  current_values=plt.gca().get_yticks()
  plt.gca().set_yticklabels(['${:,.0f}'.format(x) for x in current_values])
  plt.grid(which='major', axis='y')
  plt.grid(which='minor', axis='y')
  plt.show()

#clearbox method clears the search box when the search box is clicked on.
def clearbox(event):
    search.delete(0,"end")
    actorName.delete(0,"end")
    return None

#clrLists method clears the stored lists of movies and revenue
def clrLists():
  xaxis.clear()
  yaxis.clear()
  text.delete(1.0, "end")

#Configure Main Window
mainWindow=Tk()
#mainWindow.geometry("900x600")
mainWindow.configure(bg="magenta")
mainWindow.geometry("800x500")

#Place MovieGenie Logo
logo=Image.open('LogoMG.png')
logo=logo.resize((300,200))
logo=ImageTk.PhotoImage(logo)
logo_label=Label(image=logo, bg="#f700ff")
logo_label.image=logo
logo_label.place(x=400, y=20)

#display Heading
heading=Label(mainWindow, text="MovieGenie", bg="magenta", font=("ALGERIAN", 60))
heading.place(x=100, y=25)


#Create entry box for movie title
search=Entry(mainWindow, width=55,)
search.place(x=150, y=150)
search.insert(0, "Enter Movie Title")

#Create text box to return results
tframe=Frame(mainWindow)
tscroll=Scrollbar(tframe, orient=VERTICAL)
text=Text(tframe, width=40, height=3, yscrollcommand=tscroll.set)
tscroll.config(command=text.yview)
tscroll.pack(side=RIGHT, fill=Y)
tframe.place(x=150, y=200)
text.pack()

#Calling the clearbox method to clear the search box
search.bind("<Button-1>", clearbox)

#Button on search box to send movie title into find_Gross method
button1=Button(mainWindow, text="Enter", command=movieGross)
button1.place(x=460, y=146)
#Button to clear text box and lists
button2=Button(mainWindow,text="Clear", font=("VERDANA", 15, "bold"), command=clrLists)
button2.place(x=70, y=200)
#Button to call movieChart function and create chart
button3=Button(mainWindow, text="Make Chart", font=("VERDANA", 15,"bold"), command=movieChart)
button3.place(x=540, y=280)

#Search box for actor name
actorName=Entry(mainWindow, width=55)
actorName.place(x=150, y=300)
actorName.insert(0, "Enter Actor Name")
#clear actorName box
actorName.bind("<Button-1>", clearbox)
#button4=Button(mainWindow, text="Enter", command=filmography)
#button4.place(x=460, y=298)
mainWindow.mainloop()
