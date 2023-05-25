import customtkinter as ctk

class Menu(ctk.CTkTabview):
    def __init__(self,parent):
        super().__init__(master=parent)
        self.grid(row=0, column=0,sticky='nsew')