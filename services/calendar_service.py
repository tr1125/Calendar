from datetime import datetime, timedelta, time
from typing import List
from models.models import Meeting

# Business hour boundaries (as plain time constants)
_DAY_START_TIME = time(7, 0)
_DAY_END_TIME = time(19, 0)

def find_available_slots(person_list: List[str], event_duration: timedelta, all_meetings: List[Meeting]):
    """
    Core business logic to find free time slots for multiple participants.
    """
    # Compute datetime boundaries anchored to today, inside the function
    # so they always reflect the actual current date at call time.
    ref_date = datetime.today().date()
    DAY_START = datetime.combine(ref_date, _DAY_START_TIME)
    DAY_END = datetime.combine(ref_date, _DAY_END_TIME)

    relevant_meetings = []
    for meeting in all_meetings:
        if meeting.person_name in person_list:
            start = datetime.combine(ref_date, meeting.start_time)
            end = datetime.combine(ref_date, meeting.end_time)
            relevant_meetings.append([start, end]) 
    
    if not relevant_meetings:
        latest_start = (DAY_END - event_duration).time()
        if datetime.combine(ref_date, latest_start) >= DAY_START:
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