from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# Initialize Tkinter root
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)
root.configure(bg='#add8e6')  # Light blue background

def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)
    
    try:
        location = geolocator.geocode(city)
        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")
            
            api_key = "1f7321b35393260a2e9998bf764b3a39"  # Make sure to replace with your actual API key
            api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}"
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 403:
                messagebox.showerror("Error", f"403 Forbidden: Access is denied. Check your API key and permissions.")
                return
            
            response.raise_for_status()
            json_data = response.json()
            
            condition = json_data['weather'][0]['main']
            description = json_data['weather'][0]['description']
            temp = int(json_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            
            t.config(text=f"{temp} °C")
            c.config(text=f"{condition} | FEELS LIKE {temp} °C")
            w.config(text=f"{wind} km/h")
            h.config(text=f"{humidity} %")
            d.config(text=description.capitalize())
            p.config(text=f"{pressure} hPa")
        else:
            messagebox.showerror("Error", "City not found")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Unable to retrieve weather data: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create and style the text entry field
textfield = tk.Entry(root, justify="center", width=20, font=("Helvetica", 20, "bold"), bg="#e0ffff", bd=0, highlightthickness=2, highlightbackground="#87cefa")
textfield.place(x=70, y=40)
textfield.focus()

# Load and place the search icon button
Search_icon = PhotoImage(file="icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

# Load and place the logo image with a background color matching the window
logo_image = PhotoImage(file="Weather3.png")
logo = Label(image=logo_image, borderwidth=0, bg='#add8e6')
logo.place(x=150, y=100)

Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image, bg='#add8e6')
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
name = Label(root, font=("arial", 15, "bold"), bg='#add8e6')
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20), bg='#add8e6')
clock.place(x=30, y=130)

# Labels
label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d", bg='#add8e6')
t.place(x=550, y=150)
c = Label(font=("arial", 15, "bold"), bg='#add8e6')
c.place(x=550, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()

