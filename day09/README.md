# Assignment 9 processes

## Program
This program, saved in `main.py`, processes and analyzes GitHub issue submission data from students. It reads the `subjects.txt` file containing issue submission records and generates statistical analyses to identify patterns in when students submit their assignments.

The program performs two types of analyses:
- **By Assignment Day**: Identifies the most common submission hour and day of the week for each assignment day
- **By Student**: Identifies each student's most common submission hour and day of the week across all assignments

The program parses issue titles to extract assignment day numbers and student names, normalizes student names to handle variations, and uses the **mode** (most frequent value) to determine typical submission patterns.

## Operation
Run the program by executing `main.py`:


The program will:
1. Parse the `subjects.txt` file in the same directory
2. Extract valid submissions (excluding project proposals)
3. Display two tables showing submission patterns:
   - Submission patterns grouped by assignment day
   - Submission patterns grouped by student

### Dependencies
This project requires no external dependencies (it uses only Python standard library).

The program uses built-in modules:
- `re` (regular expressions)
- `datetime` (timestamp parsing)
- `collections` (Counter, defaultdict)
- `os` (file path handling)

### System versions
- Python 3.8+ (tested with 3.8)
- Windows (tested on Windows 10)
