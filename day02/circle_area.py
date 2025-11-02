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
# ...existing code...
root = tk.Tk()
root.title("Circle Area")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Radius:").grid(row=0, column=0, sticky="e")
entry_radius = tk.Entry(frame)
entry_radius.grid(row=0, column=1)
entry_radius.focus_set()

btn_calc = tk.Button(frame, text="Calculate", command=calculate)
btn_calc.grid(row=1, column=0, columnspan=2, pady=(8,0))

label_result = tk.Label(frame, text="Area: ")
label_result.grid(row=2, column=0, columnspan=2, pady=(8,0))

root.bind("<Return>", lambda e: calculate())
root.mainloop()


