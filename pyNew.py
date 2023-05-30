from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

# create window
window = tk.Tk()

# create frames and position side by side
frame1 = tk.Frame(master=window, width=400, height=700, bg="light grey")
frame1.pack(fill=tk.Y, side=tk.LEFT)

frame2 = tk.Frame(master=window, width=800, height=700, bg="white")
frame2.pack(fill=tk.Y, side=tk.LEFT)

frame3 = tk.Frame(master=frame1, width=400, height=200, bg="blue")
frame3.pack(expand=True, side=tk.TOP, fill=NONE)

# open and resize image to fit the window
image = Image.open("Roasted_coffee_beans.jpg")
resize_image = image.resize((800, 700))
img = ImageTk.PhotoImage(resize_image)

# Create a Label Widget to display the text or Image
label = Label(frame2, image = img)
label.pack()



window.mainloop()

