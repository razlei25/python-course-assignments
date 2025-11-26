# Copilot / AI Agent Instructions — python-course-assignments

This project contains a set of small, self-contained Python assignments organized by day (e.g. `day02`, `day03`, `day04`). Each day folder is intended to be runnable independently and usually follows a pattern: a GUI program (tkinter) that calls separate "business logic" modules. When making edits, prefer changing the business-logic module and keep the GUI thin.

Quick facts
- **Python**: 3.8+ (see `day03/pyproject.toml`, `day04/pyproject.toml`).
- **Dependencies**: `pandas` is required by `day04/stock_yield.py`. Many other days avoid third-party libs.
- **GUI toolkit**: `tkinter` (standard library) is used for UIs (`day02/shape_area_calculator.py`, `day03/main.py`, `day04/stock_yield_GUI.py`).

Project structure patterns to respect
- Each assignment is in `dayXX/`. Avoid cross-day imports unless explicitly necessary.
- GUI files (e.g. `day02/shape_area_calculator.py`, `day04/stock_yield_GUI.py`) implement the user interface only; computation logic belongs in sibling modules (e.g. `day03/shape_area_calculator_clean.py`, `day04/stock_yield.py`).
- Tests live next to the assignment they test (example: `day03/tests.py` uses `unittest`).

How to run tests and quick checks
- Run a single day's tests (PowerShell):
```
python -m unittest day03.tests
```
- Discover and run all tests from repository root:
```
python -m unittest discover -v
```
- For interactive GUI manual testing (PowerShell):
```
# run the GUI for day03
python day03/main.py
# run the GUI for day04
python day04/stock_yield_GUI.py
```

Important implementation conventions (discoverable from code)
- Validation & errors: business-logic functions raise `ValueError` or `RuntimeError` for invalid inputs rather than returning sentinel values. Example: `day03/shape_area_calculator_clean.py` raises `ValueError` for invalid polygon/circle parameters.
- Backwards-compatibility: Some modules keep older helper functions for compatibility (see `calculate_average_annual_yield` in `day04/stock_yield.py`). Preserve these unless asked to refactor.
- CSV/data files: Stock CSVs are expected in `day04/stock_data/`. Use `os.path.join(os.path.dirname(__file__), "stock_data", ...)` if you need a repo-relative default path.
- Dynamic column detection: `day04/stock_yield.py` tries multiple column names for dates and close prices — follow that approach when adding CSV parsing logic (`_find_date_and_close_columns`).

When editing code
- If you modify a business-logic function (e.g. `polygon_area`, `circle_area`, `calculate_yield_between_dates`):
  - Update or add unit tests in the same day folder (`day03/tests.py`, etc.).
  - Keep function signatures stable where possible. If changing a signature, update all callers (usually one GUI file).
- Avoid adding new third-party dependencies without updating the corresponding `dayXX/pyproject.toml` and documenting install commands in that day's `README.md`.
- Maintain the separation of concerns: GUI files should not implement new calculations. Move any new calculation code into a `dayXX/*.py` business module and import it from the GUI.

Prompts & examples for AI edits
- Add a new pure logic implementation (example):
  - "Implement `triangle_area(a, b, c)` in `day03/shape_area_calculator_clean.py` with input validation consistent with existing functions and add matching `unittest` cases in `day03/tests.py`."
- Update GUI to call business logic (example):
  - "Change `day02/shape_area_calculator.py` so it calls `day03/shape_area_calculator_clean.polygon_area` instead of computing the formula inline. Keep behaviour and validation identical."

Do not assume
- There is no global packaging or CI setup in this repo. Do not add project-wide tooling (tox/CI) unless requested.
- The root `README.md` is minimal — consult per-day `README.md` files for intent and dependency notes.

Where to look first (references)
- Business logic examples: `day03/shape_area_calculator_clean.py`, `day04/stock_yield.py`
- GUI examples: `day02/shape_area_calculator.py`, `day04/stock_yield_GUI.py`, `day03/main.py`
- Tests: `day03/tests.py`
- Day-level metadata: `day03/pyproject.toml`, `day04/pyproject.toml`, `day03/README.md`, `day04/README.md`

Questions? Ask the repository owner which day(s) to prioritize and whether new dependencies are permitted.
