#Imports
from tkinter import *
import tkinter as tk
import os
from datetime import datetime
import psutil
from PIL import ImageTk, Image
import asyncio
import python_weather
import sys

###Helper Functions
#Get date 
def getHourString():
    hour = datetime.now().hour

    #Morning Check
    if(6 < hour < 12):
        return "Morning"
    #Afternoon Check
    elif(12 <= hour < 18):
        return "Afternoon"
    #Evening Check
    else:
        return "Evening"

#Get battery percentage
def getBatteryPercentage():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent
    else:
        return None
    
percent = getBatteryPercentage()

#Get Battery Images
def getBatteryImage(percent):
    if percent is not None and percent < 35:
        return lowImg
    elif percent is not None and percent < 65:
        return halfImg
    else:
        return highImg

###Async Weather Client
#Current Temperature
async def currentTemp() -> int:

  # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    # Fetch a weather forecast from a city.
    weather = await client.get('Burke, VA')

    # Fetch the temperature for today.
    currentTemp = weather.temperature
    return currentTemp

if __name__ == '__currentTemp__':

  # See https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details.
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

  asyncio.run(currentTemp())
getCurrentTemp = lambda: asyncio.run(currentTemp())

#Get current forecast
async def currentForecast() -> str:
    # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    
        # Fetch a weather forecast from a city.
        weather = await client.get('Burke, VA')
    
        # Fetch the forecast for today.
        currentForecast = weather.kind.emoji
        return currentForecast


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Usage:
lowImg = resource_path("shhhhh/LOW.png")
halfImg = resource_path("shhhhh/HALF.png")
highImg = resource_path("shhhhh/FULL.png")

print(datetime.now().hour)
print(percent)
print(getCurrentTemp())

###Start of Application
root = Tk()
#Title
root.title("Hello Honey!")
#Window size 
root.geometry("800x600")
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(0,0)
#Background color
root.configure(background='pink')

#Giddyup Std or Terminal
###Good Morning/Afternoon/Evening, Melissa
l = Label(root, font=("Terminal", 30), bg="pink", text=("Good "+ getHourString() + ", Melissa"))
l.place(relx=.5, rely=.1, anchor=tk.CENTER)

###Battery Percentage
batLabel = Label(root, font=("Terminal", 25), bg="pink", text=(f"Battery: {percent}%"))
batLabel.place(relx=.25, rely=.35, anchor=tk.CENTER)
img = Image.open(getBatteryImage(percent))
img = img.resize((200, 200), Image.LANCZOS)
img = ImageTk.PhotoImage(img)
labelImg = Label(root, image=img, background="pink")
labelImg.place(relx=.25, rely=.55, anchor=tk.CENTER)

def update_battery():
    global percent, img
    percent = getBatteryPercentage()
    batLabel.config(text=(f"Battery: {percent}%"))
    img = Image.open(getBatteryImage(percent))
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    labelImg.config(image=img)
    labelImg.image = img  # Keep a reference to avoid garbage collection
    root.after(60000, update_battery)  # Update every minute

###Temperature
tempTextLabel = Label(root, font=("Terminal", 25), bg="pink", text=("Current Temp:"))
tempTextLabel.place(relx=.75, rely=.35, anchor=tk.CENTER)
tempLabel = Label(root, font=("Terminal", 35), bg="pink", text=(f"{getCurrentTemp()}°F"))
tempLabel.place(relx=.75, rely=.55, anchor=tk.CENTER)

#update temperature every 10 minutes
def update_temperature():
    currentTemp = getCurrentTemp()
    tempLabel.config(text=(f"{currentTemp}°F"))
    root.after(600000, update_temperature)  # Update every 10 minutes

###Date and Time
dateLabel = Label(root, font=("Terminal", 25), bg="pink", text=(datetime.now().strftime("%d/%m/%Y")))
dateLabel.place(relx=.35, rely=.2, anchor=tk.CENTER)
timeLabel = Label(root, font=("Terminal", 25), bg="pink", text=(datetime.now().strftime("%H:%M:%S")))
timeLabel.place(relx=.65, rely=.2, anchor=tk.CENTER)

#update time every second
def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    timeLabel.config(text=current_time)
    root.after(1000, update_time)

#Display current weather forecast using emoji
forecastLabel = Label(root, font=("Terminal", 25), bg="pink", text=(f"Current Forecast: {asyncio.run(currentForecast())}"))
forecastLabel.place(relx=.5, rely=.8, anchor=tk.CENTER)

#update forecast every 10 minutes
async def update_forecast():
    currentForecastEmoji = await currentForecast()
    forecastLabel.config(text=(f"Current Forecast: {currentForecastEmoji}"))
    root.after(600000, update_forecast)  # Update every 10 minutes

root.iconbitmap(resource_path("HeartIcon.ico")) 

#eof
update_forecast()
update_temperature()
update_battery()
update_time()
root.mainloop()

