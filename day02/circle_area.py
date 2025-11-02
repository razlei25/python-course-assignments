
import tkinter as tk
from tkinter import messagebox
import math

def calculate():
    try:
        r = int(entry_radius.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please write an integer")
        entry_radius.focus_set()
        return
    if r < 0:
        messagebox.showerror("Invalid input", "Please enter a non-negative number for radius.")
        entry_radius.focus_set()
        return
    area = math.pi * r * r
    label_result.config(text=f"Area: {area:.4f}")
# ...existing code...
```# filepath: c:\Users\Raz\Programming projects\Basic_Programming_Skills_Ptython_WIS\python-course-assignments\day02\circle_area.py
# ...existing code...
import tkinter as tk
from tkinter import messagebox
import math

def calculate():
    try:
        r = int(entry_radius.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please write an integer")
        entry_radius.focus_set()
        return
    if r < 0:
        messagebox.showerror("Invalid input", "Please enter a non-negative number for radius.")
        entry_radius.focus_set()
        return
    area = math.pi * r * r
    label_result.config(text=f"Area: {area:.4f}")
