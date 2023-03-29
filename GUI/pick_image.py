import tkinter as tk
from PIL import ImageTk, Image

# Create an instance of tkinter window
win = tk.Tk()

# Define the geometry of the window
win.geometry("700x500")

frame =  tk.Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk

infile = "database/examples/OH_CA_20181112_002024.tif"
img = ImageTk.PhotoImage(Image.open(infile))

# Create a Label Widget to display the text or Image
label = tk.Label(frame, image = img)
label.pack()

win.mainloop()