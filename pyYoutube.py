import tkinter
import customtkinter
from pytube import YouTube

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        finishLabel.configure(text="Downloading...")
        video.download()
        finishLabel.configure(text="Finished")
    except:
        finishLabel.configure(text="Error")

    

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size-bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion)) 
    pPercentage.configure(text=per+"%")
    pPercentage.update()

    progressBar.set(float(percentage_of_completion) / 100)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app=customtkinter.CTk()
app.geometry("500x500")
app.title("Youtube Downloader")

# UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube link", font=("Arial", 20))
title.pack(padx=10,pady=10)

# Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# finished
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# progress bar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10,pady=10)

# Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10,pady=10)

app.mainloop()