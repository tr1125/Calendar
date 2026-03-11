# repositories/csv_repository.py
import csv
import os
from datetime import datetime
from models.models import Meeting

def load_meetings(file_path: str):
    """Loads meetings from a CSV file and returns a list of Meeting objects."""
    meetings = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            # Use 1900 as base date to keep times consistent
            start_time = datetime.strptime(row[2], "%H:%M").time()
            end_time = datetime.strptime(row[3], "%H:%M").time()
            
            meetings.append(Meeting(row[0], row[1], start_time, end_time))
    return meetings