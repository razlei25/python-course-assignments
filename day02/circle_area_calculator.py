import logging
import math
import tkinter as tk
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CircleAreaApp:
    
    
    ERROR_NOT_NUMBER = "Please enter a number"
    ERROR_NEGATIVE = "Please enter a non-negative number for radius."

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Circle Area")

        self.frame = tk.Frame(self.root, padx=12, pady=12)
        self.frame.pack()

        tk.Label(self.frame, text="Radius:").grid(row=0, column=0, sticky="e")

        # Use a plain tk.Entry so we can change its background color reliably across platforms.
        self.entry_radius = tk.Entry(self.frame, width=20)
        self.entry_radius.grid(row=0, column=1)
        self.entry_radius.focus_set()

        # Save default visuals so we can restore them after an error
        self._default_bg = self.entry_radius.cget("background")
        self._default_fg = self.entry_radius.cget("foreground")

        self.btn_calc = tk.Button(self.frame, text="Calculate", command=self.calculate)
        self.btn_calc.grid(row=1, column=0, columnspan=2, pady=(8, 0))

        self.label_result = tk.Label(self.frame, text="Area: ")
        self.label_result.grid(row=2, column=0, columnspan=2, pady=(8, 0))

        # Bind Enter key to calculate
        self.root.bind("<Return>", self.calculate)

        # When the user focuses the entry, clear any error message and restore style
        self.entry_radius.bind("<FocusIn>", self._on_entry_focus_in)

    def _set_entry_error(self, message: str) -> None:
        """
        Put the error message into the entry and make the entry visually red.
        """
        logger.debug("Setting entry error: %s", message)
        # A readable red-ish background; "red" is strong, "lightcoral" is softer.
        self.entry_radius.delete(0, tk.END)
        self.entry_radius.insert(0, message)
        try:
            self.entry_radius.config(background="lightcoral")
        except tk.TclError:
            # Some platforms/themes might not allow background change; fallback to highlight
            self.entry_radius.config(highlightbackground="red", highlightthickness=1)

    def _restore_entry_style(self) -> None:
        """
        Restore the entry's original background/foreground so it looks normal again.
        """
        logger.debug("Restoring entry style to defaults")
        try:
            self.entry_radius.config(background=self._default_bg, foreground=self._default_fg)
            self.entry_radius.config(highlightthickness=0)
        except tk.TclError:
            # If platform doesn't allow, ignore silently
            pass

    def _on_entry_focus_in(self, event: Optional[tk.Event]) -> None:
        """
        If the entry currently contains one of our error messages, clear it and restore style.
        """
        current = self.entry_radius.get().strip()
        if current in {self.ERROR_NOT_NUMBER, self.ERROR_NEGATIVE}:
            logger.debug("Clearing placeholder/error text on focus")
            self.entry_radius.delete(0, tk.END)
            self._restore_entry_style()

    def calculate(self, event: Optional[tk.Event] = None) -> None:
        """
        Read the radius from entry, validate, compute the circle area, and display it.
        On invalid input, show error message inside the entry and highlight it.
        """
        raw = self.entry_radius.get().strip()
        logger.info("Calculating area for input: %r", raw)

        # Try parsing a float so numbers like "2.5" are accepted.
        try:
            radius = float(raw)
        except ValueError:
            logger.warning("Non-numeric input received: %r", raw)
            self._set_entry_error(self.ERROR_NOT_NUMBER)
            self.entry_radius.focus_set()
            return

        if radius < 0:
            logger.warning("Negative radius received: %s", radius)
            self._set_entry_error(self.ERROR_NEGATIVE)
            self.entry_radius.focus_set()
            return

        # Valid input -- compute and show result, restore style if previously errored.
        area = math.pi * radius * radius
        self.label_result.config(text=f"Area: {area:.4f}")
        self._restore_entry_style()


def main() -> None:
    root = tk.Tk()
    app = CircleAreaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()