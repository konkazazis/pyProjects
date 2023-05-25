import customtkinter as ctk

class Panel(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent, fg_color='dark gray')
        self.pack(fill='x', pady=4, ipady=8)

class SliderPanel(Panel):
    def __init__(self,parent,text):
        super().__init__(parent = parent)

        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)

        ctk.CTklabel(self,text = text).grid(column = 0, row = 0, sticky = 'W', padx = 5)
        ctk.CTklabel(self,text = '0.0').grid(column = 1, row = 0, sticky = 'E', padx = 5)
        ctk.CTkSlider(self).grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 5)