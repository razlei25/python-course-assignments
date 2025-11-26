```markdown
# Assignment 5 processes

## Foreword
This folder is a skeleton for Day 05 of the course. Implement the business logic in `program_logic.py` and the GUI in `program_GUI.py`.

## Dependencies
- Python 3.8+

Add any extra dependencies to `pyproject.toml` (the `dependencies` array) and document install commands here.

Install example (PowerShell):
```
python -m pip install --upgrade pip
# if you add dependencies, install them here, for example:
# python -m pip install pandas
```

## How to run
- Run tests (once written):
```
python -m unittest day05.tests
```
- Run the GUI (after implementing `program_logic.py`):
```
python day05/program_GUI.py
```

## AI usage
When asking an AI assistant to edit files in this folder, prefer prompts that:
- Ask to implement pure business logic in `program_logic.py`.
- Keep GUI changes in `program_GUI.py` limited to wiring inputs/outputs to the business logic.

Example prompts:
- "Implement `compute_something(arg1, arg2)` in `day05/program_logic.py` with input validation and add tests in `day05/tests.py`."
- "Update `day05/program_GUI.py` to collect user inputs, call `program_logic.compute_something`, and display the result."

``` 
