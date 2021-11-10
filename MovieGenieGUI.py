import tkinter as tk
from PIL import Image, ImageTk
mainWindow=tk.Tk()
#set canvas
canvas=tk.Canvas(mainWindow, width=800, height=500)
canvas.grid(columnspan=3)
#display logo
logo=Image.open('MGLogo.png')
logo=logo.resize((200,200))
logo=ImageTk.PhotoImage(logo)
logo_label=tk.Label(image=logo)
logo_label.image=logo
logo_label.grid(column=3, row=0)
#display Heading
heading=tk.Label(mainWindow, text="MovieGenie",font=("ALGERIAN", 25))
heading.grid(columnspan=3, column=0, row=0)
#Some code here
mainWindow.mainloop()
