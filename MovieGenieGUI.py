import tkinter as tk
from PIL import Image, ImageTk
from Get_Gross import movieGross
mainWindow=tk.Tk()
mainWindow.geometry("900x600")
mainWindow.configure(bg="magenta")
#canvas=tk.Canvas(mainWindow, width=500, height=300, bg="magenta")
#canvas.grid(columnspan=3)
#display logo
logo=Image.open('LogoMG.png')
logo=logo.resize((300,200))
logo=ImageTk.PhotoImage(logo)
logo_label=tk.Label(image=logo, bg="#f700ff")
logo_label.image=logo
logo_label.pack()
#logo_label.grid(columnspan=2, column=1, row=0)
#display Heading
heading=tk.Label(mainWindow, text="MovieGenie", bg="magenta", font=("ALGERIAN", 60))
#heading.grid(columnspan=2, column=0, row=0)
heading.pack()

search=tk.Entry(mainWindow, width=55,)
#search.grid(columnspan=3, column=0, row=1)
search.pack()
search.insert(0, "Enter Movie Title")

def do_Something():
  title=search.get()
  #display=tk.Label(mainWindow, text=(movieGross(title)))
  #display.grid(columnspan=3, column=0, row=2, pady=10, padx=10)
  #display.pack()
  text=tk.Text(mainWindow, width=60, height=2)
  text.pack()
  text.insert(1.0,(movieGross(title)))
  search.delete(0,"end")
  return None
def clearbox(event):
    search.delete(0,"end")
    return None
search.bind("<Button-1>", clearbox)
button1=tk.Button(mainWindow, text="Enter", command=do_Something)
#button1.grid(columnspan=3,column=1,row=1)
button1.pack()

mainWindow.mainloop()
