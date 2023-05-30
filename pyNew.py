from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image


window = tk.Tk()

frame1 = tk.Frame(master=window, width=400, height=700, bg="light grey")
frame1.pack(fill=tk.Y, side=tk.LEFT)

frame2 = tk.Frame(master=window, width=800, height=700, bg="white")
frame2.pack(fill=tk.Y, side=tk.LEFT)



window.mainloop()

