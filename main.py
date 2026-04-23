import customtkinter as ctk
import re
from enum import Enum
from tkcalendar import Calendar, DateEntry
from datetime import datetime

app = ctk.CTk()
app.title("University Life")
app.geometry("500x400")
ctk.set_appearance_mode("light")

scheduleFile = "schedule.txt"
notesFile = "notes.txt"

mainContainer = ctk.CTkFrame(app, fg_color="transparent")
mainContainer.pack(expand=True)

menuContainer = ctk.CTkFrame(mainContainer, fg_color="transparent")
menuContainer.pack()

def makeLabel(text, container):
    label = ctk.CTkLabel(
        container,
        text=text,
        font=("Dubai", 32, "bold"),
        text_color="#1c2b48",
        corner_radius=18
    )
    label.pack(pady=20)

def makeButton(text, container, command):
    button = ctk.CTkButton(
        container,
        text=text,
        width=250,
        font=("Dubai", 28, "bold"),
        fg_color="#5f86a6",
        text_color="#e8ecef",
        hover_color="#3f5c75",
        command=command
    )
    button.pack(pady=5)

def makeTextField(placeholderText, container):
    textField = ctk.CTkEntry(
        container,
        placeholder_text=placeholderText,
        width=250,
        height=40,
        font=("Dubai", 18, "bold"),
        fg_color="#cfe3f1",
        text_color="#333333",
    )
    textField.pack(pady=5)
    return textField

def makeGoBackButton(container, command):
    button = ctk.CTkButton(
        container,
        text="Go Back",
        width=200,
        font=("Dubai", 20, "bold"),
        fg_color="transparent",
        text_color="#243a5e",
        border_color="#0b2033",
        border_width=2,
        command=command
    )
    button.pack(pady=10)

def hideAll():
    menuContainer.pack_forget()
    scheduleWindow.pack_forget()
    notesWindow.pack_forget()
    addClassWindow.pack_forget()
    viewScheduleWindow.pack_forget()
    deleteClassWindow.pack_forget()

def saveDataButton(container, command):
    button = ctk.CTkButton (
        container,
        text="Save!",
        width=200,
        font=("Dubai", 20, "bold"),
        fg_color="transparent",
        text_color="#243a5e",
        border_color="#0b2033",
        border_width=2,
        command=command
    )
    button.pack(pady=20)


def checkInput(data, type):
    match type:
        case "text":
            return bool (re.fullmatch(r"[a-zA-Z0-9 ]+", data))
        case "numbers":
            return data.isdigit()
        case "mix":
            return bool(re.fullmatch(r"[a-zA-Z0-9 ]+", data))
        case "time":
            return bool (re.fullmatch(r"\d{2}:\d{2}", data))
        case "date":
            return bool(re.fullmatch(r"\d{2}\.\d{2}\.(\d{2}|\d{4})", data))

def showNotification(container, message, color):
    notification = ctk.CTkLabel(
        container,
        text=message,
        font=("Dubai", 14, "bold"),
        text_color="white",
        fg_color=color,
        corner_radius=8
    )
    notification.place(relx=0.5, rely=0.19, anchor="center")
    app.after(2000, notification.destroy)

def setToNullSchedule():
    classField.delete(0, "end")
    dayField.set_date(datetime.today()) 
    timeField.delete(0, "end")
    roomField.delete(0, "end")

def saveDataButtonClicked(classs, day, time, room):
    if checkInput(classs, "text") and checkInput(time, "time") and checkInput(room, "mix"):
        try:
            with open(scheduleFile, 'a') as f:
                f.write(f"{classs} - {day} - {time} - {room}\n")
            showNotification(addClassWindow, "DATA SAVED!", "#38c34a")
            setToNullSchedule()
        except Exception as e:
            showNotification(addClassWindow, f"Error: {e}", "#e74c3c")
    else:
        showNotification(mainContainer, "INVALID DATA", "#e74c3c")

def goToMenu():
    hideAll()
    menuContainer.pack()

def goToSchedule():
    hideAll()
    setToNullSchedule()
    scheduleWindow.pack()

def buttonClicked(name):
    hideAll()
    match name:
        case "scheduleButton":
            scheduleWindow.pack()
        case "notesButton":
            notesWindow.pack()


def makeText(container, text):
    text = ctk.CTkLabel(
        container,
        text=text,
        font=("Dubai", 24, "bold"),
        text_color="#e8ecef",
        anchor="n"
    )
    text.pack(anchor="n", fill="x")

def printText(container, filename):
    try:
        file = open(filename)
        for line in file:
            makeText(container, line)
    except:
        showNotification(container, "Error! Cant load schedule", "#e74c3c")


def setSchedulesPages(page):
    hideAll()
    match page:
        case "addClassWindow":
            addClassWindow.pack()
        case "viewScheduleWindow":
            for widget in viewScheduleWindow.winfo_children():
                widget.destroy()
            makeLabel("Schedule", viewScheduleWindow)
    
            scrollFrame = makeFrame(viewScheduleWindow)  
            printText(scrollFrame, scheduleFile)         
    
            makeGoBackButton(viewScheduleWindow, goToSchedule)
            viewScheduleWindow.pack()
        case "deleteClassWindow":
            deleteClassWindow.pack()

def makeFrame(container):
    frame = ctk.CTkScrollableFrame (
        container,
        width= 500,
        height= 400,
        fg_color= "#1c2b48"
    )
    frame.pack()
    return frame

def closeApp():
    app.destroy()


scheduleWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
notesWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
addClassWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")  
viewScheduleWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
deleteClassWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")

# Menu
makeLabel("UNIVERSITY LIFE PLANNER", menuContainer)
makeButton("Schedule", menuContainer, lambda: buttonClicked("scheduleButton"))
makeButton("Notes", menuContainer, lambda: buttonClicked("notesButton"))

exitButton = ctk.CTkButton(
    menuContainer, text="Exit", width=200,
    font=("Dubai", 20, "bold"), fg_color="transparent",
    text_color="#243a5e", border_color="#0b2033", border_width=2,
    command=closeApp
)
exitButton.pack(pady=5)

# Schedule Window
makeLabel("Schedule", scheduleWindow)
makeButton("Add Class", scheduleWindow, lambda: setSchedulesPages("addClassWindow"))
makeButton("View Schedule", scheduleWindow, lambda: setSchedulesPages("viewScheduleWindow"))
makeButton("Delete Class", scheduleWindow, lambda: setSchedulesPages("deleteClassWindow"))
makeGoBackButton(scheduleWindow, goToMenu)

# Add Class Window
makeLabel("Add Class", addClassWindow)

classField = makeTextField("Enter class", addClassWindow)
dayField = DateEntry(
    addClassWindow,
    width=22,
    font=("Dubai", 18, "bold"),
    fieldbackground="#cfe3f1",
    foreground="#333333",
    background="#5f86a6",
    borderwidth=0,
    date_pattern="dd.mm.yy"
)
dayField.pack(pady=5, ipady=8)
timeField  = makeTextField("Enter time",  addClassWindow)
roomField  = makeTextField("Enter room",  addClassWindow)

saveDataButton(addClassWindow, lambda: saveDataButtonClicked(classField.get(), dayField.get(), timeField.get(), roomField.get()))
makeGoBackButton(addClassWindow, goToSchedule)

# View Schedule


app.mainloop()