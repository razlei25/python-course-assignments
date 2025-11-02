import tkinter as tk
from tkinter import ttk
import math

class ShapeAreaCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Area Calculator")
        self.root.geometry("500x500")
        self.root.configure(bg="#6B46C1")  # Purple background
        
        # Main container
        self.main_frame = tk.Frame(root, bg="#6B46C1")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Shape Area Calculator",
            font=("Helvetica", 24, "bold"),
            bg="#6B46C1",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(
            self.main_frame,
            text="Choose a shape:",
            font=("Helvetica", 14),
            bg="#6B46C1",
            fg="white"
        )
        instruction_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.main_frame, bg="#6B46C1")
        button_frame.pack(pady=20)
        
        # Polygon button
        polygon_btn = tk.Button(
            button_frame,
            text="Equilateral Polygon",
            font=("Helvetica", 12, "bold"),
            bg="#9F7AEA",
            fg="white",
            activebackground="#805AD5",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.show_polygon_inputs
        )
        polygon_btn.pack(side='left', padx=10)
        
        # Circle button
        circle_btn = tk.Button(
            button_frame,
            text="Circle",
            font=("Helvetica", 12, "bold"),
            bg="#9F7AEA",
            fg="white",
            activebackground="#805AD5",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.show_circle_inputs
        )
        circle_btn.pack(side='left', padx=10)
        
        # Input frame (will be populated based on shape choice)
        self.input_frame = tk.Frame(self.main_frame, bg="#6B46C1")
        self.input_frame.pack(pady=20)
        
        # Result frame
        self.result_frame = tk.Frame(self.main_frame, bg="#6B46C1")
        self.result_frame.pack(pady=20)
        
        # Result label
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#6B46C1",
            fg="#FFD700",
            wraplength=400
        )
        self.result_label.pack()
    
    def clear_input_frame(self):
        """Clear all widgets from input frame"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
    
    def validate_positive_integer(self, value, entry_widget):
        """Validate if value is a positive integer"""
        if not value:  # Empty string
            entry_widget.config(bg="#FC8181")
            return False
            
        try:
            num = int(value)
            if num <= 0:
                entry_widget.config(bg="#FC8181")
                return False
            else:
                entry_widget.config(bg="white")
                return True
        except ValueError:
            entry_widget.config(bg="#FC8181")
            return False
    
    def show_polygon_inputs(self):
        """Display input fields for equilateral polygon"""
        self.clear_input_frame()
        
        # Number of sides
        sides_label = tk.Label(
            self.input_frame,
            text="Number of sides:",
            font=("Helvetica", 12),
            bg="#6B46C1",
            fg="white"
        )
        sides_label.grid(row=0, column=0, pady=5, padx=10, sticky='e')
        
        self.sides_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 12),
            width=20,
            justify='center',
            bg="white"
        )
        self.sides_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Side length
        length_label = tk.Label(
            self.input_frame,
            text="Side length:",
            font=("Helvetica", 12),
            bg="#6B46C1",
            fg="white"
        )
        length_label.grid(row=1, column=0, pady=5, padx=10, sticky='e')
        
        self.length_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 12),
            width=20,
            justify='center',
            bg="white"
        )
        self.length_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Calculate button
        calc_btn = tk.Button(
            self.input_frame,
            text="Calculate Area",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            activebackground="#38A169",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.calculate_polygon_area
        )
        calc_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
    def show_circle_inputs(self):
        """Display input field for circle"""
        self.clear_input_frame()
        
        # Radius
        radius_label = tk.Label(
            self.input_frame,
            text="Radius:",
            font=("Helvetica", 12),
            bg="#6B46C1",
            fg="white"
        )
        radius_label.grid(row=0, column=0, pady=5, padx=10, sticky='e')
        
        self.radius_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 12),
            width=20,
            justify='center',
            bg="white"
        )
        self.radius_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Calculate button
        calc_btn = tk.Button(
            self.input_frame,
            text="Calculate Area",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            activebackground="#38A169",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.calculate_circle_area
        )
        calc_btn.grid(row=1, column=0, columnspan=2, pady=20)
    
    def calculate_polygon_area(self):
        """Calculate area of equilateral polygon"""
        sides_value = self.sides_entry.get()
        length_value = self.length_entry.get()
        
        print(f"Polygon - Sides: {sides_value}, Length: {length_value}")  # Debug
        
        sides_valid = self.validate_positive_integer(sides_value, self.sides_entry)
        length_valid = self.validate_positive_integer(length_value, self.length_entry)
        
        if not sides_valid:
            self.sides_entry.delete(0, tk.END)
            self.sides_entry.insert(0, "Must be positive integer")
            
        if not length_valid:
            self.length_entry.delete(0, tk.END)
            self.length_entry.insert(0, "Must be positive integer")
        
        if sides_valid and length_valid:
            n = int(sides_value)
            s = int(length_value)
            
            # Formula for area of regular polygon: (n * s^2) / (4 * tan(π/n))
            area = (n * s**2) / (4 * math.tan(math.pi / n))
            
            result_text = f"Area: {area:.2f} square units"
            print(f"Setting result: {result_text}")  # Debug
            self.result_label.config(text=result_text)
    
    def calculate_circle_area(self):
        """Calculate area of circle"""
        radius_value = self.radius_entry.get()
        
        print(f"Circle - Radius: {radius_value}")  # Debug
        
        radius_valid = self.validate_positive_integer(radius_value, self.radius_entry)
        
        if not radius_valid:
            self.radius_entry.delete(0, tk.END)
            self.radius_entry.insert(0, "Must be positive integer")
        
        if radius_valid:
            r = int(radius_value)
            area = math.pi * r**2
            
            result_text = f"Area: {area:.2f} square units"
            print(f"Setting result: {result_text}")  # Debug
            self.result_label.config(text=result_text)

def main():
    root = tk.Tk()
    app = ShapeAreaCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()