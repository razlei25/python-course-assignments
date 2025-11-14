import tkinter as tk
from tkinter import ttk
import shape_area_calculator_clean as calc


class ShapeAreaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Area Calculator")
        self.root.geometry("500x600")
        self.root.configure(bg="#6B46C1")  # Purple background

        self.main_frame = tk.Frame(root, bg="#6B46C1")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(
            self.main_frame,
            text="Shape Area Calculator",
            font=("Helvetica", 24, "bold"),
            bg="#6B46C1",
            fg="white",
        ).pack(pady=20)

        tk.Label(
            self.main_frame,
            text="Choose a shape:",
            font=("Helvetica", 14),
            bg="#6B46C1",
            fg="white",
        ).pack(pady=10)

        button_frame = tk.Frame(self.main_frame, bg="#6B46C1")
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Equilateral Polygon",
            font=("Helvetica", 12, "bold"),
            bg="#9F7AEA",
            fg="white",
            activebackground="#805AD5",
            relief="flat",
            padx=20,
            pady=10,
            command=self.show_polygon_inputs,
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Circle",
            font=("Helvetica", 12, "bold"),
            bg="#9F7AEA",
            fg="white",
            activebackground="#805AD5",
            relief="flat",
            padx=20,
            pady=10,
            command=self.show_circle_inputs,
        ).pack(side="left", padx=10)

        self.input_frame = tk.Frame(self.main_frame, bg="#6B46C1")
        self.input_frame.pack(pady=20)

        self.result_label = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#6B46C1",
            fg="#FFD700",
            wraplength=400,
        )
        self.result_label.pack(pady=10)

    def clear_inputs(self):
        for w in self.input_frame.winfo_children():
            w.destroy()
        self.result_label.config(text="")

    def _set_entry_error(self, entry: tk.Entry, msg: str) -> None:
        entry.delete(0, tk.END)
        entry.insert(0, msg)
        entry.config(bg="#FC8181")

    def _restore_entry(self, entry: tk.Entry) -> None:
        entry.config(bg="white")

    def show_polygon_inputs(self):
        self.clear_inputs()
        tk.Label(
            self.input_frame, text="Number of sides:", font=("Helvetica", 12), bg="#6B46C1", fg="white"
        ).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.sides_entry = tk.Entry(self.input_frame, width=20, justify="center", bg="white")
        self.sides_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            self.input_frame, text="Side length:", font=("Helvetica", 12), bg="#6B46C1", fg="white"
        ).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.length_entry = tk.Entry(self.input_frame, width=20, justify="center", bg="white")
        self.length_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            self.input_frame,
            text="Calculate Area",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.calculate_polygon,
        ).grid(row=2, column=0, columnspan=2, pady=20)

        # restore style on focus
        self.sides_entry.bind("<FocusIn>", lambda e: self._restore_entry(self.sides_entry))
        self.length_entry.bind("<FocusIn>", lambda e: self._restore_entry(self.length_entry))
        self.root.bind("<Return>", lambda e: self.calculate_polygon())

    def show_circle_inputs(self):
        self.clear_inputs()
        tk.Label(
            self.input_frame, text="Radius:", font=("Helvetica", 12), bg="#6B46C1", fg="white"
        ).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.radius_entry = tk.Entry(self.input_frame, width=20, justify="center", bg="white")
        self.radius_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            self.input_frame,
            text="Calculate Area",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.calculate_circle,
        ).grid(row=1, column=0, columnspan=2, pady=20)

        self.radius_entry.bind("<FocusIn>", lambda e: self._restore_entry(self.radius_entry))
        self.root.bind("<Return>", lambda e: self.calculate_circle())

    def calculate_polygon(self):
        # Validate and call calculation from shape_calculations module
        sides = self.sides_entry.get().strip()
        length = self.length_entry.get().strip()

        try:
            n = int(sides)
        except Exception:
            self._set_entry_error(self.sides_entry, "Must be integer > 2")
            return

        try:
            s = float(length)
        except Exception:
            self._set_entry_error(self.length_entry, "Must be positive number")
            return

        try:
            area = calc.polygon_area(n, s)
        except ValueError as exc:
            # show which entry is invalid
            msg = str(exc)
            if "sides" in msg.lower():
                self._set_entry_error(self.sides_entry, "Must be integer > 2")
            else:
                self._set_entry_error(self.length_entry, "Must be positive number")
            return

        self.result_label.config(text=f"Area: {area:.2f} square units", fg="#FFD700")

    def calculate_circle(self):
        radius = self.radius_entry.get().strip()
        try:
            r = float(radius)
        except Exception:
            self._set_entry_error(self.radius_entry, "Must be positive number")
            return

        try:
            area = calc.circle_area(r)
        except ValueError:
            self._set_entry_error(self.radius_entry, "Must be positive number")
            return

        self.result_label.config(text=f"Area: {area:.2f} square units", fg="#FFD700")


def main():
    root = tk.Tk()
    app = ShapeAreaGUI(root)
    root.mainloop()



if __name__ == "__main__":
    main()
