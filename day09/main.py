import re
from datetime import datetime
from collections import Counter, defaultdict
import os


def parse_subjects_file(filepath):
    """Parse the subjects.txt file and extract submission data."""
    submissions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split by tabs (there may be multiple tabs)
            parts = [p for p in line.split('\t') if p]
            if len(parts) < 4:
                continue
            
            issue_num = parts[0].strip()
            status = parts[1].strip()
            title = parts[2].strip()
            timestamp = parts[3].strip()
            
            if not timestamp:
                continue
            
            # Skip project proposals
            if 'proposal' in title.lower() or 'project' in title.lower():
                continue
            
            # Extract day number and student name from title
            # Pattern: day[number] by [name]
            match = re.search(r'day\s*(\d+)\s+by\s+(.+)', title, re.IGNORECASE)
            if not match:
                continue
            
            day_num = int(match.group(1))
            student_name = match.group(2).strip()
            
            # Normalize student name (handle case, extra spaces, dashes)
            student_name = normalize_name(student_name)
            
            # Parse timestamp
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            submissions.append({
                'day': day_num,
                'student': student_name,
                'timestamp': dt,
                'hour': dt.hour,
                'weekday': dt.strftime('%A')
            })
    
    return submissions


def normalize_name(name):
    """Normalize student names to handle variations."""
    # Convert to title case for consistency
    name = name.strip()
    
    # Handle special cases and variations
    name = name.replace('-', ' ')  # Convert dashes to spaces
    name = re.sub(r'\s+', ' ', name)  # Normalize spaces
    
    # Split into parts and capitalize each part
    parts = name.split()
    normalized_parts = [part.capitalize() for part in parts]
    
    return ' '.join(normalized_parts)


def calculate_mode(values):
    """Calculate the mode (most common value) from a list."""
    if not values:
        return None
    counter = Counter(values)
    mode_value, _ = counter.most_common(1)[0]
    return mode_value


def analyze_by_day(submissions):
    """Analyze submissions grouped by assignment day."""
    day_data = defaultdict(lambda: {'hours': [], 'weekdays': []})
    
    for sub in submissions:
        day_data[sub['day']]['hours'].append(sub['hour'])
        day_data[sub['day']]['weekdays'].append(sub['weekday'])
    
    results = {}
    for day in sorted(day_data.keys()):
        mode_hour = calculate_mode(day_data[day]['hours'])
        mode_weekday = calculate_mode(day_data[day]['weekdays'])
        results[day] = {
            'mode_hour': mode_hour,
            'mode_weekday': mode_weekday
        }
    
    return results


def analyze_by_student(submissions):
    """Analyze submissions grouped by student."""
    student_data = defaultdict(lambda: {'hours': [], 'weekdays': []})
    
    for sub in submissions:
        student_data[sub['student']]['hours'].append(sub['hour'])
        student_data[sub['student']]['weekdays'].append(sub['weekday'])
    
    results = {}
    for student in sorted(student_data.keys()):
        mode_hour = calculate_mode(student_data[student]['hours'])
        mode_weekday = calculate_mode(student_data[student]['weekdays'])
        results[student] = {
            'mode_hour': mode_hour,
            'mode_weekday': mode_weekday
        }
    
    return results


def print_day_table(day_results):
    """Print table with results grouped by day."""
    print("\n" + "="*60)
    print("SUBMISSION PATTERNS BY ASSIGNMENT DAY")
    print("="*60)
    print(f"{'Day':<10} {'Mode Hour':<20} {'Mode Day of Week':<30}")
    print("-"*60)
    
    for day in sorted(day_results.keys()):
        mode_hour = day_results[day]['mode_hour']
        mode_weekday = day_results[day]['mode_weekday']
        hour_str = f"{mode_hour:02d}:00" if mode_hour is not None else "N/A"
        weekday_str = mode_weekday if mode_weekday else "N/A"
        print(f"Day {day:02d}    {hour_str:<20} {weekday_str:<30}")
    
    print("="*60)


def print_student_table(student_results):
    """Print table with results grouped by student."""
    print("\n" + "="*70)
    print("SUBMISSION PATTERNS BY STUDENT")
    print("="*70)
    print(f"{'Student Name':<30} {'Mode Hour':<20} {'Mode Day of Week':<20}")
    print("-"*70)
    
    for student in sorted(student_results.keys()):
        mode_hour = student_results[student]['mode_hour']
        mode_weekday = student_results[student]['mode_weekday']
        hour_str = f"{mode_hour:02d}:00" if mode_hour is not None else "N/A"
        weekday_str = mode_weekday if mode_weekday else "N/A"
        print(f"{student:<30} {hour_str:<20} {weekday_str:<20}")
    
    print("="*70)


def main():
    # Get the path to subjects.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subjects_file = os.path.join(script_dir, 'subjects.txt')
    
    # Parse submissions
    print("Parsing subjects.txt...")
    submissions = parse_subjects_file(subjects_file)
    print(f"Found {len(submissions)} valid submissions")
    
    # Analyze by day
    day_results = analyze_by_day(submissions)
    print_day_table(day_results)
    
    # Analyze by student
    student_results = analyze_by_student(submissions)
    print_student_table(student_results)


if __name__ == "__main__":
    main()
