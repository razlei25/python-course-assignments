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


## Example Output
```
============================================================
SUBMISSION PATTERNS BY ASSIGNMENT DAY
============================================================
Day        Mode Hour            Mode Day of Week
------------------------------------------------------------
Day 01    20:00                Wednesday
Day 02    09:00                Friday
Day 03    18:00                Saturday
Day 04    15:00                Saturday
Day 05    15:00                Saturday
Day 06    22:00                Saturday
Day 08    18:00                Tuesday
============================================================

======================================================================
SUBMISSION PATTERNS BY STUDENT
======================================================================
Student Name                   Mode Hour            Mode Day of Week 

----------------------------------------------------------------------
Achinoam Shoham                15:00                Wednesday        

Adi Moses                      15:00                Saturday         

Adib Masharqa                  16:00                Saturday         

Aileen Cohen                   15:00                Saturday         

Anvita Pant                    09:00                Monday           

Arad Zulti                     15:00                Saturday         

Ariel Hindi                    22:00                Saturday         

Avigail Yariv                  08:00                Saturday         

Daniela Huppert Revach         15:00                Saturday         

David Ganem                    15:00                Saturday         

Einav Litvak                   15:00                Saturday         

Evyatar Shaked                 12:00                Sunday           

Guy Saller                     20:00                Wednesday        

Guy Shemesh                    22:00                Wednesday        

Guy Vosco                      13:00                Tuesday          

Hallel Azulai                  18:00                Saturday         

Inbar Perets                   16:00                Saturday         

Lihi Bolokan                   21:00                Saturday         

Lior Batat                     15:00                Saturday         

Neta Hanuka                    20:00                Saturday         

Noam Ariel                     16:00                Sunday           

Noga Levinson                  19:00                Wednesday        

Noya Levy                      15:00                Wednesday        

Rachel Steinitz Eliyahu        21:00                Saturday         

Raz Leibson                    09:00                Saturday         

Rony Holdengreber              09:00                Sunday           

Sana Khatib                    14:00                Saturday         

Sharonelle Sasson              22:00                Wednesday        

Shelly Gilad                   15:00                Saturday         

Shoshana Sernik                15:00                Saturday         

Sriashwin Sridharan            20:00                Saturday         

Yana Lerner                    09:00                Saturday         

======================================================================
```
