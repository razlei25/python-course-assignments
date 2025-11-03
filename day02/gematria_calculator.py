import tkinter as tk
from tkinter import ttk

# Define a dictionary for Hebrew Gematria values
hebrew_gematria = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400
}

# Define a dictionary for simple English Gematria (A=1, B=2, etc.)
english_gematria = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17,
    'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
    'Z': 26
}

def calculate_gematria(word, gematria_dict):
    """Calculates the gematria value of a word using a given Gematria dictionary."""
    total_value = 0
    for letter in word.upper():  # Convert to uppercase for English Gematria
        total_value += gematria_dict.get(letter, 0)  # Use .get() to handle non-alphabetic characters
    return total_value


class GematriaCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gematria Calculator")
        self.root.geometry("500x450")
        self.root.configure(bg="#4A90E2")  # Blue background
        
        # Main frame
        self.main_frame = tk.Frame(root, bg="#4A90E2")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Gematria Calculator",
            font=("Helvetica", 24, "bold"),
            bg="#4A90E2",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Instruction
        instruction_label = tk.Label(
            self.main_frame,
            text="Enter a word and select the language:",
            font=("Helvetica", 12),
            bg="#4A90E2",
            fg="white"
        )
        instruction_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.main_frame, bg="#4A90E2")
        input_frame.pack(pady=10)
        
        # Word entry
        word_label = tk.Label(
            input_frame,
            text="Word:",
            font=("Helvetica", 12),
            bg="#4A90E2",
            fg="white"
        )
        word_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        
        self.word_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=25,
            justify='center',
            bg="white"
        )
        self.word_entry.grid(row=0, column=1, padx=10, pady=5)
        self.word_entry.focus_set()
        
        # Language selection
        language_label = tk.Label(
            input_frame,
            text="Language:",
            font=("Helvetica", 12),
            bg="#4A90E2",
            fg="white"
        )
        language_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        
        self.language_var = tk.StringVar(value="Hebrew")
        
        language_frame = tk.Frame(input_frame, bg="#4A90E2")
        language_frame.grid(row=1, column=1, padx=10, pady=5)
        
        hebrew_radio = tk.Radiobutton(
            language_frame,
            text="Hebrew",
            variable=self.language_var,
            value="Hebrew",
            font=("Helvetica", 11),
            bg="#4A90E2",
            fg="white",
            selectcolor="#2C5AA0",
            activebackground="#4A90E2",
            activeforeground="white"
        )
        hebrew_radio.pack(side='left', padx=10)
        
        english_radio = tk.Radiobutton(
            language_frame,
            text="English",
            variable=self.language_var,
            value="English",
            font=("Helvetica", 11),
            bg="#4A90E2",
            fg="white",
            selectcolor="#2C5AA0",
            activebackground="#4A90E2",
            activeforeground="white"
        )
        english_radio.pack(side='left', padx=10)
        
        # Calculate button
        calc_btn = tk.Button(
            self.main_frame,
            text="Calculate Gematria",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            activebackground="#38A169",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.calculate
        )
        calc_btn.pack(pady=20)
        
        # Result frame
        self.result_frame = tk.Frame(self.main_frame, bg="#4A90E2")
        self.result_frame.pack(pady=20)
        
        # Result label
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#4A90E2",
            fg="#FFD700",
            wraplength=400
        )
        self.result_label.pack()
        
        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.calculate())
    
    def calculate(self):
        """Calculate the gematria value based on selected language"""
        word = self.word_entry.get().strip()
        
        if not word:
            self.result_label.config(
                text="Please enter a word!",
                fg="#FF6B6B"
            )
            return
        
        language = self.language_var.get()
        
        if language == "Hebrew":
            value = calculate_gematria(word, hebrew_gematria)
            self.result_label.config(
                text=f"Gematria value of '{word}' (Hebrew): {value}",
                fg="#FFD700"
            )
        else:  # English
            value = calculate_gematria(word, english_gematria)
            self.result_label.config(
                text=f"Gematria value of '{word}' (English): {value}",
                fg="#FFD700"
            )


def main():
    root = tk.Tk()
    app = GematriaCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()