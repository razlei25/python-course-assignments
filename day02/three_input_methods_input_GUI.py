import tkinter as tk
from tkinter import messagebox


class NameCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Name Checker")
        self.root.geometry("400x250")
        self.root.configure(bg="#6B46C1")  # Purple background
        
        # Main frame
        self.main_frame = tk.Frame(root, bg="#6B46C1")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Name Checker",
            font=("Helvetica", 20, "bold"),
            bg="#6B46C1",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Question label
        question_label = tk.Label(
            self.main_frame,
            text="What is your name?",
            font=("Helvetica", 14),
            bg="#6B46C1",
            fg="white"
        )
        question_label.pack(pady=10)
        
        # Entry field
        self.name_entry = tk.Entry(
            self.main_frame,
            font=("Helvetica", 12),
            width=25,
            justify='center',
            bg="white"
        )
        self.name_entry.pack(pady=10)
        self.name_entry.focus_set()
        
        # Submit button
        submit_btn = tk.Button(
            self.main_frame,
            text="Submit",
            font=("Helvetica", 12, "bold"),
            bg="#48BB78",
            fg="white",
            activebackground="#38A169",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.check_name
        )
        submit_btn.pack(pady=10)
        
        # Bind Enter key to submit
        self.root.bind("<Return>", lambda event: self.check_name())
    
    def check_name(self):
        """Check if the entered name is Bob"""
        answer = self.name_entry.get().strip()
        
        if not answer:
            messagebox.showwarning("Empty Name", "Please enter a name!")
            return
        
        if answer == "Bob":
            messagebox.showinfo(
                "Welcome Bob!",
                "It is so nice to finally meet you Bob! I hate other people."
            )
            self.root.quit()
        else:
            response = messagebox.askyesno(
                "Not Bob",
                f"Hello, {answer}, I was hoping that you are Bob.\n\nWould you like to try again?"
            )
            
            if response:  # User clicked Yes
                self.name_entry.delete(0, tk.END)
                self.name_entry.focus_set()
            else:  # User clicked No
                messagebox.showinfo(
                    "Goodbye",
                    "I hoped you'd say that... Bob would have never given up"
                )
                self.root.quit()


def main():
    root = tk.Tk()
    app = NameCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
