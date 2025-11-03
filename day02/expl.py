import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageTk, ImageDraw
import random
import math
import ephem

def create_starry_background(width, height):
    # Create a dark blue background
    image = Image.new('RGB', (width, height), '#000033')
    draw = ImageDraw.Draw(image)
    
    # Add stars
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(180, 255)
        color = (brightness, brightness, brightness)
        draw.ellipse([x, y, x + size, y + size], fill=color)
    
    return ImageTk.PhotoImage(image)

def get_zodiac_sign_from_angle(angle):
    zodiac_ranges = [
        (0, "♈ Aries"), (30, "♉ Taurus"), (60, "♊ Gemini"),
        (90, "♋ Cancer"), (120, "♌ Leo"), (150, "♍ Virgo"),
        (180, "♎ Libra"), (210, "♏ Scorpio"), (240, "♐ Sagittarius"),
        (270, "♑ Capricorn"), (300, "♒ Aquarius"), (330, "♓ Pisces"), (360, "♈ Aries")
    ]
    for i in range(len(zodiac_ranges)-1):
        if zodiac_ranges[i][0] <= angle < zodiac_ranges[i+1][0]:
            return zodiac_ranges[i][1]
    return zodiac_ranges[0][1]

def get_moon_sign(date, lat, lon):
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = date.strftime('%Y/%m/%d %H:%M:%S')
    moon = ephem.Moon()
    moon.compute(observer)
    # Convert moon longitude to degrees
    degrees = math.degrees(moon.elong) % 360
    return get_zodiac_sign_from_angle(degrees)

def get_rising_sign(date, lat, lon):
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = date.strftime('%Y/%m/%d %H:%M:%S')
    sun = ephem.Sun()
    sun.compute(observer)
    # Calculate ascendant
    rasc = observer.sidereal_time() - sun.ra + math.pi
    degrees = math.degrees(rasc) % 360
    return get_zodiac_sign_from_angle(degrees)

def get_sun_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "♈ Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "♉ Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "♊ Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "♋ Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "♌ Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "♍ Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "♎ Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "♏ Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "♐ Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "♑ Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "♒ Aquarius"
    else:
        return "♓ Pisces"

def get_sign_description(sign):
    descriptions = {
        "♈ Aries": "Dynamic, confident, and adventurous. Natural leader with boundless energy.",
        "♉ Taurus": "Reliable, patient, and determined. Appreciates beauty and comfort.",
        "♊ Gemini": "Versatile, expressive, and curious. Quick-witted communicator.",
        "♋ Cancer": "Nurturing, intuitive, and emotional. Deep connection to home and family.",
        "♌ Leo": "Charismatic, generous, and proud. Born leader with a flair for drama.",
        "♍ Virgo": "Analytical, practical, and perfectionist. Detail-oriented problem solver.",
        "♎ Libra": "Harmonious, diplomatic, and charming. Seeks balance and beauty.",
        "♏ Scorpio": "Intense, passionate, and transformative. Deeply emotional and mysterious.",
        "♐ Sagittarius": "Optimistic, adventurous, and philosophical. Seeker of truth and wisdom.",
        "♑ Capricorn": "Ambitious, disciplined, and patient. Natural manager and achiever.",
        "♒ Aquarius": "Innovative, independent, and humanitarian. Forward-thinking visionary.",
        "♓ Pisces": "Compassionate, artistic, and intuitive. Deeply spiritual and empathetic."
    }
    return descriptions.get(sign, "Unknown sign")

def create_zodiac_gui():
    def calculate_profile():
        try:
            # Get date and time from entry fields
            date_str = f"{date_entry.get()} {time_entry.get()}"
            date_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
            
            # Get location
            try:
                lat = float(lat_entry.get())
                lon = float(lon_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid latitude and longitude")
                return
            
            # Calculate sun sign
            day = date_obj.day
            month = date_obj.month
            sun_sign = get_sun_sign(day, month)
            
            # Calculate moon and rising signs
            moon_sign = get_moon_sign(date_obj, lat, lon)
            rising_sign = get_rising_sign(date_obj, lat, lon)
            
            # Clear previous results
            result_text.delete(1.0, tk.END)
            
            # Add new results with formatting
            result_text.insert(tk.END, "✨ Your Zodiac Profile ✨\n\n", 'title')
            
            result_text.insert(tk.END, "Sun Sign (Core Identity):\n", 'title')
            result_text.insert(tk.END, f"{sun_sign}\n", 'sign')
            result_text.insert(tk.END, f"{get_sign_description(sun_sign)}\n\n", 'description')
            
            result_text.insert(tk.END, "Moon Sign (Emotional Nature):\n", 'title')
            result_text.insert(tk.END, f"{moon_sign}\n", 'sign')
            result_text.insert(tk.END, f"{get_sign_description(moon_sign)}\n\n", 'description')
            
            result_text.insert(tk.END, "Rising Sign (External Persona):\n", 'title')
            result_text.insert(tk.END, f"{rising_sign}\n", 'sign')
            result_text.insert(tk.END, f"{get_sign_description(rising_sign)}\n\n", 'description')
            
            # Make text read-only
            result_text.configure(state='disabled')
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter date in format DD/MM/YYYY and time in format HH:MM")

    # Create main window
    root = tk.Tk()
    root.title("✨ Zodiac Profile Calculator ✨")
    
    # Set window size
    width = 600
    height = 800
    root.geometry(f"{width}x{height}")

    # Create and set background
    bg_image = create_starry_background(width, height)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Create main frame
    frame = tk.Frame(root, bg='#000033', bd=2)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Create and pack widgets with mystical styling
    title_label = tk.Label(frame,
                          text="✨ Your Complete Zodiac Profile ✨",
                          font=('Helvetica', 20, 'bold'),
                          fg='#FFD700',
                          bg='#000033')
    title_label.pack(pady=20)

    # Date input
    date_frame = tk.Frame(frame, bg='#000033')
    date_frame.pack(fill='x', padx=20)
    
    date_label = tk.Label(date_frame,
                         text="Birth Date (DD/MM/YYYY):",
                         font=('Helvetica', 12),
                         fg='#FFD700',
                         bg='#000033')
    date_label.pack()
    
    date_entry = ttk.Entry(date_frame, font=('Helvetica', 12))
    date_entry.pack(pady=5)

    # Time input
    time_label = tk.Label(date_frame,
                         text="Birth Time (HH:MM):",
                         font=('Helvetica', 12),
                         fg='#FFD700',
                         bg='#000033')
    time_label.pack()
    
    time_entry = ttk.Entry(date_frame, font=('Helvetica', 12))
    time_entry.pack(pady=5)

    # Location input with help text
    location_frame = tk.Frame(frame, bg='#000033')
    location_frame.pack(fill='x', padx=20, pady=10)
    
    location_help = tk.Label(location_frame,
                           text="To find your coordinates:\n1. Open Google Maps\n2. Right-click your location\n3. Use the numbers in the popup",
                           font=('Helvetica', 10),
                           fg='#B8860B',
                           bg='#000033',
                           justify='left')
    location_help.pack(pady=5)
    
    lat_label = tk.Label(location_frame,
                        text="Latitude:",
                        font=('Helvetica', 12),
                        fg='#FFD700',
                        bg='#000033',
                        wraplength=400,
                        justify='left')
    lat_label.pack()
    
    lat_entry = ttk.Entry(location_frame, font=('Helvetica', 12))
    lat_entry.pack(pady=5)
    
    lon_label = tk.Label(location_frame,
                        text="Longitude:",
                        font=('Helvetica', 12),
                        fg='#FFD700',
                        bg='#000033',
                        wraplength=400,
                        justify='left')
    lon_label.pack()
    
    lon_entry = ttk.Entry(location_frame, font=('Helvetica', 12))
    lon_entry.pack(pady=5)
    
    # Add some example locations
    examples_label = tk.Label(location_frame,
                            text="Example coordinates:\nNew York: 40.7128, -74.0060\nTokyo: 35.6762, 139.6503\nSydney: -33.8688, 151.2093",
                            font=('Helvetica', 10),
                            fg='#B8860B',
                            bg='#000033',
                            justify='left')
    examples_label.pack(pady=5)

    calculate_button = tk.Button(frame,
                               text="🌟 Reveal Zodiac Profile 🌟",
                               command=calculate_profile,
                               font=('Helvetica', 12, 'bold'),
                               bg='#4A0080',
                               fg='#FFD700',
                               activebackground='#6B238E',
                               activeforeground='#FFD700',
                               relief='raised',
                               bd=3)
    calculate_button.pack(pady=20)

    # Create result frame with scrollable text
    result_frame = tk.Frame(frame, bg='#000033', bd=2)
    result_frame.pack(fill='both', expand=True, padx=20, pady=10)

    result_text = tk.Text(result_frame,
                         font=('Helvetica', 12),
                         fg='#FFD700',
                         bg='#000033',
                         wrap=tk.WORD,
                         height=10,
                         width=40)
    result_text.pack(pady=10)
    result_text.tag_configure('title', font=('Helvetica', 14, 'bold'))
    result_text.tag_configure('sign', font=('Helvetica', 12, 'bold'))
    result_text.tag_configure('description', font=('Helvetica', 10, 'italic'))

    # Keep a reference to prevent garbage collection
    root.bg_image = bg_image
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    create_zodiac_gui()