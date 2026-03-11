"""
This is the App entry point
"""
import sys
from typing import List
from datetime import time, timedelta, datetime
import csv
import os
from .Meeting import Meeting

_REF_DATE = datetime.today().date()
DAY_START = datetime.combine(_REF_DATE, datetime.strptime("07:00", "%H:%M").time())
DAY_END   = datetime.combine(_REF_DATE, datetime.strptime("19:00", "%H:%M").time())
meetings_list = []

def load_meets_from_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'resources', 'calendar.csv')
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                if not row or len(row) < 4:
                    continue
                
                try:
                    start_time_obj = datetime.strptime(row[2], "%H:%M").time()
                    end_time_obj = datetime.strptime(row[3], "%H:%M").time()
                except ValueError:
                    start_time_obj = datetime.strptime(row[2], "%H:%M:%S").time()
                    end_time_obj = datetime.strptime(row[3], "%H:%M:%S").time()

                new_meet = Meeting(row[0], row[1], start_time_obj, end_time_obj) 
                meetings_list.append(new_meet)

    except FileNotFoundError:
        print(f"שגיאה: הקובץ לא נמצא בנתיב {csv_path}")

    print(f"נטענו {len(meetings_list)} פגישות.")

def find_available_slots(person_list: List[str], event_duration: timedelta, all_meetings: List[Meeting] = None) -> List[tuple]:
    if all_meetings is None:
        all_meetings = meetings_list
        
    relevant_meetings = []
    for meeting in all_meetings:
        if meeting.person_name in person_list:
            # המרה לאובייקט datetime לצורך חישובים
            start = datetime.combine(datetime.today(), meeting.start_time)
            end = datetime.combine(datetime.today(), meeting.end_time)
            relevant_meetings.append([start, end]) 
    
    if not relevant_meetings:
        latest_start = (DAY_END - event_duration).time()
        if datetime.combine(datetime.today(), latest_start) >= DAY_START:
            return [(DAY_START.time(), latest_start)]
        return []
    
    relevant_meetings.sort()
    merged = []
    curr_start, curr_end = relevant_meetings[0]

    for next_start, next_end in relevant_meetings[1:]:
        if next_start < curr_end:
            curr_end = max(curr_end, next_end)
        else:
            merged.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end
    merged.append((curr_start, curr_end))

    available_windows = []
    last_end = DAY_START

    for start, end in merged:
        window_start = max(last_end, DAY_START)
        if start - window_start >= event_duration:
            latest_possible_start = start - event_duration
            available_windows.append((window_start.time(), latest_possible_start.time()))
        
        last_end = max(last_end, end)

    if DAY_END - last_end >= event_duration:
        latest_possible_start = DAY_END - event_duration
        available_windows.append((last_end.time(), latest_possible_start.time()))

    return available_windows

    


def main():
    load_meets_from_csv()
    person_list = ["Alice", "Bob", "Jack"]
    event_duration = timedelta(hours=1)
    available_slots = find_available_slots(person_list, event_duration)
    
    print("Available slots for Alice, Bob, and Jack:")
    for start, end in available_slots:
        print(f"{start} - {end}")


if __name__ == "__main__":
    main()
