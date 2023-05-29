import customtkinter as ctk
import ebooklib
from ebooklib import epub
from tkinter import *

root = Tk()

book = epub.read_epub('test.epub')

for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
    print(image)


root.mainloop()